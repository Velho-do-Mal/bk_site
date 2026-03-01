from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('missao-visao-valores/', views.missao_visao, name='missao_visao'),
    path('tecnologia-bim/', views.tecnologia, name='tecnologia'),
]
