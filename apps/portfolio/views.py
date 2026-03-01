from django.shortcuts import render, get_object_or_404
from .models import CategoriaPortfolio, Projeto

def lista(request):
    categoria_slug = request.GET.get('categoria', '')
    categorias = CategoriaPortfolio.objects.all()
    projetos = Projeto.objects.filter(ativo=True)
    if categoria_slug:
        projetos = projetos.filter(categoria__slug=categoria_slug)
    return render(request, 'portfolio/lista.html', {
        'projetos': projetos, 'categorias': categorias,
        'categoria_ativa': categoria_slug})

def detalhe(request, slug):
    projeto = get_object_or_404(Projeto, slug=slug, ativo=True)
    relacionados = Projeto.objects.filter(
        categoria=projeto.categoria, ativo=True).exclude(id=projeto.id)[:3]
    return render(request, 'portfolio/detalhe.html', {
        'projeto': projeto, 'relacionados': relacionados})
