from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.blog.models import Artigo
from apps.portfolio.models import Projeto
from apps.servicos.models import Servico


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            'core:home', 'core:sobre', 'core:missao_visao', 'core:tecnologia',
            'contato:contato', 'portfolio:lista', 'blog:lista',
            'loja:produtos', 'loja:softwares',
        ]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Artigo.objects.filter(status='publicado')

    def lastmod(self, obj):
        return obj.atualizado_em

    def location(self, obj):
        return reverse('blog:detalhe', kwargs={'slug': obj.slug})


class PortfolioSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Projeto.objects.filter(ativo=True)

    def location(self, obj):
        return reverse('portfolio:detalhe', kwargs={'slug': obj.slug})


class ServicosSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Servico.objects.filter(ativo=True)

    def location(self, obj):
        return reverse('servicos:detalhe', kwargs={'slug': obj.slug})
