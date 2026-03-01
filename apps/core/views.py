from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from .models import Depoimento, Parceiro, Numero
from apps.blog.models import Artigo
from apps.portfolio.models import Projeto


def home(request):
    numeros = Numero.objects.filter(ativo=True)
    depoimentos = Depoimento.objects.filter(ativo=True)
    parceiros = Parceiro.objects.filter(ativo=True)
    projetos_destaque = Projeto.objects.filter(ativo=True, destaque=True)[:6]
    artigos_recentes = Artigo.objects.filter(status='publicado').order_by('-publicado_em')[:3]

    return render(request, 'core/home.html', {
        'numeros': numeros,
        'depoimentos': depoimentos,
        'parceiros': parceiros,
        'projetos_destaque': projetos_destaque,
        'artigos_recentes': artigos_recentes,
        'tools_list': ['AutoCAD', 'Revit', 'PLS-CADD', 'ETAP', 'Python', 'PTW', 'SEL', 'BIM'],
    })


def sobre(request):
    return render(request, 'core/sobre.html')


def missao_visao(request):
    return render(request, 'core/missao_visao.html')


def tecnologia(request):
    return render(request, 'core/tecnologia.html')
