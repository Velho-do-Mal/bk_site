"""BK Engenharia — URLs principal"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from apps.core.sitemaps import (
    StaticViewSitemap, BlogSitemap, PortfolioSitemap, ServicosSitemap
)

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'portfolio': PortfolioSitemap,
    'servicos': ServicosSitemap,
}

# URLs sem prefixo de idioma
urlpatterns = [
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain'
    )),
]

# URLs com prefixo de idioma (/pt-br/, /en/, /es/)
urlpatterns += i18n_patterns(
    path('', include('apps.core.urls')),
    path('servicos/', include('apps.servicos.urls')),
    path('portfolio/', include('apps.portfolio.urls')),
    path('loja/', include('apps.loja.urls')),
    path('blog/', include('apps.blog.urls')),
    path('contato/', include('apps.contato.urls')),
    path('cliente/', include('apps.accounts.urls')),
    prefix_default_language=False,  # pt-br não precisa de prefixo
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
