import logging
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Contato

logger = logging.getLogger(__name__)


def contato(request):
    if request.method == 'POST':
        nome     = request.POST.get('nome', '').strip()
        empresa  = request.POST.get('empresa', '').strip()
        email    = request.POST.get('email', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        assunto  = request.POST.get('assunto', 'outro').strip()
        mensagem = request.POST.get('mensagem', '').strip()

        # Validação mínima
        if not nome or not email or not mensagem:
            messages.error(request, _('Preencha os campos obrigatórios: Nome, E-mail e Mensagem.'))
            return render(request, 'contato/contato.html', {
                'assuntos': Contato.ASSUNTO_CHOICES,
                'form_data': request.POST,
            })

        # 1. Salvar no banco — bloco isolado para não depender do e-mail
        contato_obj = None
        try:
            contato_obj = Contato.objects.create(
                nome=nome,
                empresa=empresa,
                email=email,
                telefone=telefone,
                assunto=assunto,
                mensagem=mensagem,
                ip=request.META.get('REMOTE_ADDR'),
            )
            logger.info(f'Contato salvo: {contato_obj.pk} — {nome} ({email})')
        except Exception as db_err:
            logger.error(f'Erro ao salvar contato no banco: {db_err}')

        # 2. Enviar e-mail de notificação — falha silenciosa, nunca derruba o form
        assunto_display = dict(Contato.ASSUNTO_CHOICES).get(assunto, assunto)
        try:
            email_host_user = getattr(settings, 'EMAIL_HOST_USER', '')
            email_host_pass = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
            contact_email   = getattr(settings, 'CONTACT_EMAIL', 'marcio@bk-engenharia.com')

            if email_host_user and email_host_pass:
                send_mail(
                    subject=f'[BK Site] {assunto_display} — {nome}',
                    message=(
                        f'Novo contato recebido pelo site.\n\n'
                        f'Nome:     {nome}\n'
                        f'Empresa:  {empresa or "—"}\n'
                        f'E-mail:   {email}\n'
                        f'Telefone: {telefone or "—"}\n'
                        f'Assunto:  {assunto_display}\n\n'
                        f'Mensagem:\n{mensagem}'
                    ),
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', email_host_user),
                    recipient_list=[contact_email],
                    fail_silently=True,
                )
                logger.info(f'E-mail de notificação enviado para {contact_email}')
            else:
                logger.warning('EMAIL_HOST_USER ou EMAIL_HOST_PASSWORD não configurados.')
        except Exception as mail_err:
            logger.error(f'Erro ao enviar e-mail de notificação: {mail_err}')

        # 3. Sempre redireciona com mensagem de sucesso
        messages.success(request, _(
            'Mensagem enviada com sucesso! Márcio retornará em até 24 horas.'
        ))
        return redirect('contato:contato')

    return render(request, 'contato/contato.html', {
        'assuntos': Contato.ASSUNTO_CHOICES,
    })
