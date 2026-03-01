from django.shortcuts import render, get_object_or_404
from .models import CategoriaServico, Servico

def lista(request):
    categorias = CategoriaServico.objects.prefetch_related('servicos').filter(
        servicos__ativo=True).distinct().order_by('ordem')
    return render(request, 'servicos/lista.html', {'categorias': categorias})

def detalhe(request, slug):
    servico = get_object_or_404(Servico, slug=slug, ativo=True)
    servicos_relacionados = Servico.objects.filter(
        categoria=servico.categoria, ativo=True).exclude(id=servico.id)[:4]
    inclui_padrao = ['Memória de Cálculo', 'Estudos Técnicos', 'Documentação ABNT', 'Acompanhamento', 'ART do Responsável']
    return render(request, 'servicos/detalhe.html', {
        'servico': servico,
        'servicos_relacionados': servicos_relacionados,
        'inclui_padrao': inclui_padrao,
    })
