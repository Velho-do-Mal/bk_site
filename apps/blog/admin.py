from django.contrib import admin
from . import models
from django.apps import apps as django_apps

app_config = django_apps.get_app_config('blog')
for model in app_config.get_models():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
