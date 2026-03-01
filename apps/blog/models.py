from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class CategoriaBlog(models.Model):
    nome = models.CharField(_('Nome'), max_length=80)
    slug = models.SlugField(unique=True)
    descricao = models.CharField(_('Descrição'), max_length=200, blank=True)

    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Tag(models.Model):
    nome = models.CharField(_('Nome'), max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.nome


class Artigo(models.Model):
    STATUS_CHOICES = [('rascunho', _('Rascunho')), ('publicado', _('Publicado'))]

    titulo = models.CharField(_('Título'), max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey(CategoriaBlog, on_delete=models.SET_NULL,
                                   null=True, related_name='artigos')
    tags = models.ManyToManyField(Tag, blank=True)
    resumo = models.TextField(_('Resumo'), max_length=400,
                               help_text='Aparece no card e no meta description (SEO)')
    conteudo = RichTextUploadingField(_('Conteúdo'))
    imagem_capa = models.ImageField(_('Imagem capa'), upload_to='blog/')
    status = models.CharField(_('Status'), max_length=20,
                               choices=STATUS_CHOICES, default='rascunho')
    meta_description = models.CharField(_('Meta Description'), max_length=160, blank=True,
                                         help_text='Deixe vazio para usar o resumo')
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=250, blank=True)
    publicado_em = models.DateTimeField(_('Publicado em'), blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    visualizacoes = models.IntegerField(_('Visualizações'), default=0)

    class Meta:
        verbose_name = _('Artigo')
        verbose_name_plural = _('Artigos')
        ordering = ['-publicado_em']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        if not self.meta_description:
            self.meta_description = self.resumo[:160]
        super().save(*args, **kwargs)

    def get_meta_description(self):
        return self.meta_description or self.resumo[:160]
