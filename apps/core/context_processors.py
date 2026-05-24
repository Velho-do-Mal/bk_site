from django.conf import settings


def site_config(request):
    return {
        'SITE_NAME': 'BK Engenharia e Tecnologia',
        'SITE_PHONE': '(48) 98877-3776',
        'SITE_EMAIL': 'marcio@bk-engenharia.com',
        'SITE_WHATSAPP': getattr(settings, 'WHATSAPP_NUMBER', '5548988773776'),
        'SITE_ADDRESS': 'Florianópolis — SC, Brasil',
        'SITE_LINKEDIN': 'https://linkedin.com/company/bk-engenharia',
        'SITE_INSTAGRAM': 'https://instagram.com/bkengenharia',
    }
