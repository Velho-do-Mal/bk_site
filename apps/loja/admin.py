from django.contrib import admin
from .models import (CategoriaLoja, Produto, ImagemProduto, Software,
                     Pedido, ItemPedido)

class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('subtotal',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'estoque', 'ativo', 'destaque')
    list_editable = ('ativo', 'destaque', 'estoque')
    list_filter = ('categoria', 'ativo', 'destaque')
    search_fields = ('nome', 'sku')
    prepopulated_fields = {'slug': ('nome',)}
    inlines = [ImagemProdutoInline]

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_mensal', 'preco_anual', 'ativo', 'destaque')
    prepopulated_fields = {'slug': ('nome',)}

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'nome', 'email', 'total', 'status', 'criado_em')
    list_filter = ('status',)
    search_fields = ('numero', 'nome', 'email')
    readonly_fields = ('numero', 'mp_payment_id', 'mp_status')
    inlines = [ItemPedidoInline]

admin.site.register(CategoriaLoja)
