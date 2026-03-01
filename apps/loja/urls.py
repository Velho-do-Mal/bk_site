from django.urls import path
from . import views

app_name = 'loja'

urlpatterns = [
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/<slug:slug>/', views.detalhe_produto, name='detalhe_produto'),
    path('softwares/', views.softwares, name='softwares'),
    path('softwares/<slug:slug>/', views.detalhe_software, name='detalhe_software'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/adicionar/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<str:key>/', views.remover_carrinho, name='remover_carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('webhook/', views.webhook_mp, name='webhook_mp'),
    path('pedido/<str:numero>/sucesso/', views.pedido_sucesso, name='pedido_sucesso'),
    path('pedido/<str:numero>/falha/', views.pedido_falha, name='pedido_falha'),
]
