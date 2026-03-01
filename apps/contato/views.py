from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Contato


def contato(request):
    if request.method == 'POST':
        try:
            c = Contato.objects.create(
                nome=request.POST.get('nome', ''),
                empresa=request.POST.get('empresa', ''),
                email=request.POST.get('email', ''),
                telefone=request.POST.get('telefone', ''),
                assunto=request.POST.get('assunto', 'outro'),
                mensagem=request.POST.get('mensagem', ''),
                ip=request.META.get('REMOTE_ADDR'),
            )
            # Email interno
            send_mail(
                subject=f'[BK Site] {c.get_assunto_display()} — {c.nome}',
                message=f'De: {c.nome} ({c.empresa})\nEmail: {c.email}\nTel: {c.telefone}\n\n{c.mensagem}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=True,
            )
            messages.success(request, _('Mensagem enviada! Retornaremos em breve.'))
            return redirect('contato:contato')
        except Exception as e:
            messages.error(request, _('Erro ao enviar. Tente novamente.'))

    return render(request, 'contato/contato.html', {
        'assuntos': Contato.ASSUNTO_CHOICES,
    })
