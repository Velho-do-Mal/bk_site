from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Artigo, CategoriaBlog, Tag

def lista(request):
    artigos = Artigo.objects.filter(status='publicado').order_by('-publicado_em')
    categoria_slug = request.GET.get('categoria', '')
    if categoria_slug:
        artigos = artigos.filter(categoria__slug=categoria_slug)
    paginator = Paginator(artigos, 9)
    page = paginator.get_page(request.GET.get('page'))
    categorias = CategoriaBlog.objects.all()
    return render(request, 'blog/lista.html', {
        'page_obj': page, 'categorias': categorias, 'categoria_ativa': categoria_slug})

def detalhe(request, slug):
    artigo = get_object_or_404(Artigo, slug=slug, status='publicado')
    artigo.visualizacoes += 1
    artigo.save(update_fields=['visualizacoes'])
    relacionados = Artigo.objects.filter(
        status='publicado', categoria=artigo.categoria
    ).exclude(id=artigo.id)[:3]
    return render(request, 'blog/detalhe.html', {
        'artigo': artigo, 'relacionados': relacionados})
