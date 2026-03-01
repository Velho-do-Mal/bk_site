import json
import mercadopago
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Produto, Software, CategoriaLoja, Pedido, ItemPedido


def produtos(request):
    categoria_slug = request.GET.get('categoria', '')
    categorias = CategoriaLoja.objects.filter(tipo='produto', ativo=True)
    prods = Produto.objects.filter(ativo=True, categoria__tipo='produto')
    if categoria_slug:
        prods = prods.filter(categoria__slug=categoria_slug)
    return render(request, 'loja/produtos.html', {
        'produtos': prods, 'categorias': categorias, 'categoria_ativa': categoria_slug})


def detalhe_produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug, ativo=True)
    relacionados = Produto.objects.filter(
        categoria=produto.categoria, ativo=True).exclude(id=produto.id)[:4]
    mp_public_key = settings.MERCADOPAGO_PUBLIC_KEY
    return render(request, 'loja/detalhe_produto.html', {
        'produto': produto, 'relacionados': relacionados,
        'mp_public_key': mp_public_key})


def softwares(request):
    softs = Software.objects.filter(ativo=True)
    return render(request, 'loja/softwares.html', {'softwares': softs})


def detalhe_software(request, slug):
    software = get_object_or_404(Software, slug=slug, ativo=True)
    return render(request, 'loja/detalhe_software.html', {'software': software})


def carrinho(request):
    cart = request.session.get('carrinho', {})
    itens = []
    total = 0
    for item_key, item in cart.items():
        subtotal = item['preco'] * item['quantidade']
        total += subtotal
        itens.append({**item, 'subtotal': subtotal, 'key': item_key})
    return render(request, 'loja/carrinho.html', {'itens': itens, 'total': total})


def adicionar_carrinho(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo', 'produto')
        item_id = request.POST.get('id')
        quantidade = int(request.POST.get('quantidade', 1))

        if tipo == 'produto':
            obj = get_object_or_404(Produto, id=item_id, ativo=True)
            key = f'produto_{item_id}'
        else:
            obj = get_object_or_404(Software, id=item_id, ativo=True)
            key = f'software_{item_id}'

        cart = request.session.get('carrinho', {})
        if key in cart:
            cart[key]['quantidade'] += quantidade
        else:
            preco = float(obj.preco) if tipo == 'produto' else float(obj.preco_mensal or 0)
            cart[key] = {
                'tipo': tipo, 'id': int(item_id),
                'nome': obj.nome, 'preco': preco,
                'quantidade': quantidade,
                'imagem': str(obj.imagem_capa) if obj.imagem_capa else '',
            }
        request.session['carrinho'] = cart
        request.session.modified = True

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            total_itens = sum(i['quantidade'] for i in cart.values())
            return JsonResponse({'ok': True, 'total_itens': total_itens})

    return redirect('loja:carrinho')


def remover_carrinho(request, key):
    cart = request.session.get('carrinho', {})
    cart.pop(key, None)
    request.session['carrinho'] = cart
    request.session.modified = True
    return redirect('loja:carrinho')


def checkout(request):
    cart = request.session.get('carrinho', {})
    if not cart:
        messages.warning(request, _('Seu carrinho está vazio.'))
        return redirect('loja:produtos')

    total = sum(i['preco'] * i['quantidade'] for i in cart.values())
    mp_public_key = settings.MERCADOPAGO_PUBLIC_KEY

    if request.method == 'POST':
        # Criar pedido
        pedido = Pedido.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            email=request.POST.get('email'),
            nome=request.POST.get('nome'),
            cpf=request.POST.get('cpf', ''),
            telefone=request.POST.get('telefone', ''),
            endereco=request.POST.get('endereco', ''),
            cep=request.POST.get('cep', ''),
            total=total,
        )
        for key, item in cart.items():
            ItemPedido.objects.create(
                pedido=pedido,
                produto_id=item['id'] if item['tipo'] == 'produto' else None,
                software_id=item['id'] if item['tipo'] == 'software' else None,
                nome_item=item['nome'],
                quantidade=item['quantidade'],
                preco_unitario=item['preco'],
            )

        # Criar preferência MercadoPago
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        items_mp = [
            {
                'title': i['nome'], 'quantity': i['quantidade'],
                'unit_price': float(i['preco']),
                'currency_id': 'BRL',
            }
            for i in cart.values()
        ]
        preference_data = {
            'items': items_mp,
            'payer': {'email': pedido.email, 'name': pedido.nome},
            'payment_methods': {
                'installments': 6,
                'excluded_payment_types': [],
            },
            'back_urls': {
                'success': request.build_absolute_uri(f'/loja/pedido/{pedido.numero}/sucesso/'),
                'failure': request.build_absolute_uri(f'/loja/pedido/{pedido.numero}/falha/'),
                'pending': request.build_absolute_uri(f'/loja/pedido/{pedido.numero}/pendente/'),
            },
            'auto_return': 'approved',
            'external_reference': pedido.numero,
            'notification_url': request.build_absolute_uri('/loja/webhook/'),
        }
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response['response']

        request.session['carrinho'] = {}
        request.session.modified = True

        return redirect(preference.get('init_point', '/'))

    return render(request, 'loja/checkout.html', {
        'cart': cart, 'total': total, 'mp_public_key': mp_public_key})


@csrf_exempt
def webhook_mp(request):
    """Recebe notificações do MercadoPago e atualiza status do pedido."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data.get('type') == 'payment':
                sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
                payment_id = data['data']['id']
                payment = sdk.payment().get(payment_id)['response']
                ref = payment.get('external_reference', '')
                status = payment.get('status', '')
                Pedido.objects.filter(numero=ref).update(
                    mp_payment_id=str(payment_id),
                    mp_status=status,
                    status='pago' if status == 'approved' else 'pendente',
                )
        except Exception:
            pass
    return JsonResponse({'ok': True})


def pedido_sucesso(request, numero):
    pedido = get_object_or_404(Pedido, numero=numero)
    return render(request, 'loja/pedido_sucesso.html', {'pedido': pedido})


def pedido_falha(request, numero):
    pedido = get_object_or_404(Pedido, numero=numero)
    return render(request, 'loja/pedido_falha.html', {'pedido': pedido})
