from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class CategoriaPortfolio(models.Model):
    nome = models.CharField(_('Nome'), max_length=80)
    slug = models.SlugField(unique=True)
    icone = models.CharField(_('Ícone'), max_length=60, blank=True)
    ordem = models.IntegerField(_('Ordem'), default=0)

    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Projeto(models.Model):
    TENSAO_CHOICES = [
        ('13.8kV', '13,8 kV'), ('34.5kV', '34,5 kV'), ('69kV', '69 kV'),
        ('138kV', '138 kV'), ('230kV', '230 kV'), ('500kV', '500 kV'),
        ('outro', 'Outro'),
    ]

    titulo = models.CharField(_('Título'), max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    categoria = models.ForeignKey(CategoriaPortfolio, on_delete=models.SET_NULL,
                                   null=True, related_name='projetos')
    cliente = models.CharField(_('Cliente'), max_length=120, blank=True)
    local = models.CharField(_('Local'), max_length=120, blank=True)
    tensao = models.CharField(_('Tensão'), max_length=20, choices=TENSAO_CHOICES, blank=True)
    ano = models.IntegerField(_('Ano'), blank=True, null=True)
    descricao = models.TextField(_('Descrição'))
    destaques = models.TextField(_('Destaques técnicos'), blank=True,
                                  help_text='Um por linha')
    imagem_capa = models.ImageField(_('Imagem capa'), upload_to='portfolio/')
    imagens = models.ManyToManyField('ImagemProjeto', blank=True)
    destaque = models.BooleanField(_('Em destaque'), default=False)
    ativo = models.BooleanField(_('Ativo'), default=True)
    ordem = models.IntegerField(_('Ordem'), default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Projeto')
        verbose_name_plural = _('Projetos')
        ordering = ['-destaque', '-ano', 'ordem']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def get_destaques_lista(self):
        return [d.strip() for d in self.destaques.split('\n') if d.strip()]


class ImagemProjeto(models.Model):
    imagem = models.ImageField(_('Imagem'), upload_to='portfolio/fotos/')
    legenda = models.CharField(_('Legenda'), max_length=200, blank=True)

    class Meta:
        verbose_name = _('Imagem do Projeto')
        verbose_name_plural = _('Imagens do Projeto')

    def __str__(self):
        return self.legenda or str(self.imagem)
