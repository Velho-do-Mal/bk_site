from django.db import models
from django.utils.translation import gettext_lazy as _


class Depoimento(models.Model):
    nome = models.CharField(_('Nome'), max_length=100)
    empresa = models.CharField(_('Empresa'), max_length=100)
    cargo = models.CharField(_('Cargo'), max_length=100, blank=True)
    texto = models.TextField(_('Depoimento'))
    foto = models.ImageField(_('Foto'), upload_to='depoimentos/', blank=True, null=True)
    estrelas = models.IntegerField(_('Estrelas'), default=5, choices=[(i, i) for i in range(1, 6)])
    ativo = models.BooleanField(_('Ativo'), default=True)
    ordem = models.IntegerField(_('Ordem'), default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Depoimento')
        verbose_name_plural = _('Depoimentos')
        ordering = ['ordem', '-criado_em']

    def __str__(self):
        return f'{self.nome} — {self.empresa}'


class Parceiro(models.Model):
    nome = models.CharField(_('Nome'), max_length=100)
    logo = models.ImageField(_('Logo'), upload_to='parceiros/')
    url = models.URLField(_('Site'), blank=True)
    ativo = models.BooleanField(_('Ativo'), default=True)
    ordem = models.IntegerField(_('Ordem'), default=0)

    class Meta:
        verbose_name = _('Parceiro / Cliente')
        verbose_name_plural = _('Parceiros / Clientes')
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class Numero(models.Model):
    """KPIs exibidos na home (28+ colaboradores, 50+ projetos etc.)"""
    titulo = models.CharField(_('Título'), max_length=80)
    valor = models.CharField(_('Valor'), max_length=20, help_text='Ex: 50+, 138kV, 100%')
    descricao = models.CharField(_('Descrição'), max_length=120)
    icone = models.CharField(_('Ícone'), max_length=60, blank=True,
                              help_text='Classe Heroicons, ex: bolt')
    ordem = models.IntegerField(_('Ordem'), default=0)
    ativo = models.BooleanField(_('Ativo'), default=True)

    class Meta:
        verbose_name = _('Número / KPI')
        verbose_name_plural = _('Números / KPIs')
        ordering = ['ordem']

    def __str__(self):
        return f'{self.valor} — {self.titulo}'
