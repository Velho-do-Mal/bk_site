from django.conf import settings


def site_config(request):
    return {
        'SITE_NAME': 'BK Engenharia e Tecnologia',
        'SITE_PHONE': '(41) 99527-5570',
        'SITE_EMAIL': 'marcio@bk-engenharia.com',
        'SITE_WHATSAPP': getattr(settings, 'WHATSAPP_NUMBER', '5541995275570'),
        'SITE_ADDRESS': 'Curitiba — PR, Brasil',
        'SITE_LINKEDIN': 'https://linkedin.com/company/bk-engenharia',
        'SITE_INSTAGRAM': 'https://instagram.com/bkengenharia',
    }
