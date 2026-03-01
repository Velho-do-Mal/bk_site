from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import uuid


class CategoriaLoja(models.Model):
    TIPO_CHOICES = [('produto', _('Produto')), ('software', _('Software'))]

    nome = models.CharField(_('Nome'), max_length=100)
    slug = models.SlugField(unique=True)
    tipo = models.CharField(_('Tipo'), max_length=20, choices=TIPO_CHOICES, default='produto')
    descricao = models.CharField(_('Descrição'), max_length=200, blank=True)
    icone = models.CharField(_('Ícone'), max_length=60, blank=True)
    ordem = models.IntegerField(_('Ordem'), default=0)
    ativo = models.BooleanField(_('Ativo'), default=True)

    class Meta:
        verbose_name = _('Categoria da Loja')
        verbose_name_plural = _('Categorias da Loja')
        ordering = ['tipo', 'ordem', 'nome']

    def __str__(self):
        return f'[{self.get_tipo_display()}] {self.nome}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Produto(models.Model):
    categoria = models.ForeignKey(CategoriaLoja, on_delete=models.SET_NULL,
                                   null=True, related_name='produtos')
    nome = models.CharField(_('Nome'), max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    descricao_curta = models.CharField(_('Descrição curta'), max_length=300)
    descricao = models.TextField(_('Descrição completa'))
    especificacoes = models.TextField(_('Especificações técnicas'), blank=True,
                                       help_text='Uma por linha: Tensão: 220V')
    preco = models.DecimalField(_('Preço'), max_digits=10, decimal_places=2)
    preco_original = models.DecimalField(_('Preço original (riscado)'), max_digits=10,
                                          decimal_places=2, blank=True, null=True)
    estoque = models.IntegerField(_('Estoque'), default=0)
    sku = models.CharField(_('SKU'), max_length=50, unique=True, blank=True)
    imagem_capa = models.ImageField(_('Imagem principal'), upload_to='loja/produtos/')
    ativo = models.BooleanField(_('Ativo'), default=True)
    destaque = models.BooleanField(_('Em destaque'), default=False)
    parcelas = models.IntegerField(_('Parcelas máx. sem juros'), default=6)
    peso_kg = models.DecimalField(_('Peso (kg)'), max_digits=6, decimal_places=3,
                                    blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')
        ordering = ['-destaque', 'nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        if not self.sku:
            self.sku = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    @property
    def tem_desconto(self):
        return self.preco_original and self.preco_original > self.preco

    @property
    def desconto_pct(self):
        if self.tem_desconto:
            return int((1 - self.preco / self.preco_original) * 100)
        return 0

    @property
    def em_estoque(self):
        return self.estoque > 0

    def get_especificacoes_lista(self):
        linhas = [l.strip() for l in self.especificacoes.split('\n') if ':' in l.strip()]
        return [{'chave': l.split(':')[0].strip(), 'valor': ':'.join(l.split(':')[1:]).strip()}
                for l in linhas]


class ImagemProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(_('Imagem'), upload_to='loja/produtos/fotos/')
    legenda = models.CharField(_('Legenda'), max_length=200, blank=True)
    ordem = models.IntegerField(_('Ordem'), default=0)

    class Meta:
        ordering = ['ordem']


class Software(models.Model):
    LICENCA_CHOICES = [
        ('mensal', _('Assinatura Mensal')),
        ('anual', _('Assinatura Anual')),
        ('vitalicio', _('Licença Vitalícia')),
    ]

    categoria = models.ForeignKey(CategoriaLoja, on_delete=models.SET_NULL,
                                   null=True, related_name='softwares')
    nome = models.CharField(_('Nome'), max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(_('Tagline'), max_length=200)
    descricao = models.TextField(_('Descrição'))
    funcionalidades = models.TextField(_('Funcionalidades'), blank=True,
                                        help_text='Uma por linha')
    preco_mensal = models.DecimalField(_('Preço mensal'), max_digits=8, decimal_places=2,
                                        blank=True, null=True)
    preco_anual = models.DecimalField(_('Preço anual'), max_digits=8, decimal_places=2,
                                       blank=True, null=True)
    preco_vitalicio = models.DecimalField(_('Preço vitalício'), max_digits=8, decimal_places=2,
                                           blank=True, null=True)
    imagem_capa = models.ImageField(_('Imagem / Screenshot'), upload_to='loja/softwares/')
    demo_url = models.URLField(_('URL Demo'), blank=True)
    ativo = models.BooleanField(_('Ativo'), default=True)
    destaque = models.BooleanField(_('Em destaque'), default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Software')
        verbose_name_plural = _('Softwares')
        ordering = ['-destaque', 'nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def get_funcionalidades_lista(self):
        return [f.strip() for f in self.funcionalidades.split('\n') if f.strip()]


# ── Carrinho e Pedidos ────────────────────────────────────────────────────────

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', _('Pendente')),
        ('pago', _('Pago')),
        ('enviado', _('Enviado')),
        ('entregue', _('Entregue')),
        ('cancelado', _('Cancelado')),
    ]

    numero = models.CharField(_('Número'), max_length=20, unique=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(_('E-mail'))
    nome = models.CharField(_('Nome completo'), max_length=200)
    cpf = models.CharField(_('CPF'), max_length=14, blank=True)
    telefone = models.CharField(_('Telefone'), max_length=20, blank=True)
    endereco = models.TextField(_('Endereço de entrega'), blank=True)
    cep = models.CharField(_('CEP'), max_length=9, blank=True)
    status = models.CharField(_('Status'), max_length=20,
                               choices=STATUS_CHOICES, default='pendente')
    total = models.DecimalField(_('Total'), max_digits=10, decimal_places=2, default=0)
    mp_payment_id = models.CharField(_('ID Pagamento MP'), max_length=100, blank=True)
    mp_status = models.CharField(_('Status MP'), max_length=50, blank=True)
    observacoes = models.TextField(_('Observações'), blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Pedido')
        verbose_name_plural = _('Pedidos')
        ordering = ['-criado_em']

    def __str__(self):
        return f'Pedido #{self.numero} — {self.nome}'

    def save(self, *args, **kwargs):
        if not self.numero:
            import random, string
            self.numero = 'BK' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True)
    software = models.ForeignKey(Software, on_delete=models.SET_NULL, null=True, blank=True)
    nome_item = models.CharField(_('Nome'), max_length=200)
    quantidade = models.IntegerField(_('Quantidade'), default=1)
    preco_unitario = models.DecimalField(_('Preço unitário'), max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario
