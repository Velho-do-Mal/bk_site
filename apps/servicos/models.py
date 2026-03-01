from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class CategoriaServico(models.Model):
    nome = models.CharField(_('Nome'), max_length=100)
    slug = models.SlugField(unique=True)
    icone = models.CharField(_('Ícone SVG/Heroicons'), max_length=80, blank=True)
    descricao = models.CharField(_('Descrição'), max_length=200, blank=True)
    ordem = models.IntegerField(_('Ordem'), default=0)

    class Meta:
        verbose_name = _('Categoria de Serviço')
        verbose_name_plural = _('Categorias de Serviços')
        ordering = ['ordem']

    def __str__(self):
        return self.nome


class Servico(models.Model):
    categoria = models.ForeignKey(CategoriaServico, on_delete=models.SET_NULL,
                                   null=True, related_name='servicos')
    nome = models.CharField(_('Nome'), max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    descricao_curta = models.CharField(_('Descrição curta'), max_length=250)
    descricao = models.TextField(_('Descrição completa'))
    inclui = models.TextField(_('O que inclui'), blank=True, help_text='Um item por linha')
    normas = models.CharField(_('Normas aplicáveis'), max_length=300, blank=True)
    imagem = models.ImageField(_('Imagem'), upload_to='servicos/', blank=True, null=True)
    destaque = models.BooleanField(_('Em destaque'), default=False)
    ativo = models.BooleanField(_('Ativo'), default=True)
    ordem = models.IntegerField(_('Ordem'), default=0)
    meta_description = models.CharField(_('Meta Description'), max_length=160, blank=True)

    class Meta:
        verbose_name = _('Serviço')
        verbose_name_plural = _('Serviços')
        ordering = ['categoria__ordem', 'ordem', 'nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def get_inclui_lista(self):
        return [i.strip() for i in self.inclui.split('\n') if i.strip()]
