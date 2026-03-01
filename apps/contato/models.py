from django.db import models
from django.utils.translation import gettext_lazy as _


class Contato(models.Model):
    ASSUNTO_CHOICES = [
        ('orcamento', _('Solicitar Orçamento')),
        ('projeto_eletrico', _('Projeto Elétrico')),
        ('subestacao', _('Subestação')),
        ('linha_transmissao', _('Linha de Transmissão')),
        ('software', _('Software BK')),
        ('produto', _('Produto')),
        ('parceria', _('Parceria Comercial')),
        ('outro', _('Outro')),
    ]

    nome = models.CharField(_('Nome'), max_length=120)
    empresa = models.CharField(_('Empresa'), max_length=120, blank=True)
    email = models.EmailField(_('E-mail'))
    telefone = models.CharField(_('Telefone / WhatsApp'), max_length=20, blank=True)
    assunto = models.CharField(_('Assunto'), max_length=30, choices=ASSUNTO_CHOICES)
    mensagem = models.TextField(_('Mensagem'))
    respondido = models.BooleanField(_('Respondido'), default=False)
    ip = models.GenericIPAddressField(_('IP'), blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Contato')
        verbose_name_plural = _('Contatos')
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.nome} — {self.get_assunto_display()}'
