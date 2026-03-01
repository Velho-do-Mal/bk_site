"""
python manage.py seed_data
Cria categorias e serviços iniciais baseados no portfólio BK.
"""
from django.core.management.base import BaseCommand
from apps.servicos.models import CategoriaServico, Servico
from apps.portfolio.models import CategoriaPortfolio
from apps.loja.models import CategoriaLoja


class Command(BaseCommand):
    help = 'Carrega dados iniciais da BK Engenharia'

    def handle(self, *args, **kwargs):
        self.stdout.write('Criando dados iniciais...')

        cat_proj, _ = CategoriaServico.objects.get_or_create(nome='Projetos Elétricos', defaults={'slug': 'projetos-eletricos', 'ordem': 1})
        cat_est, _ = CategoriaServico.objects.get_or_create(nome='Estudos Elétricos', defaults={'slug': 'estudos-eletricos', 'ordem': 2})
        cat_exec, _ = CategoriaServico.objects.get_or_create(nome='Execução e Gestão', defaults={'slug': 'execucao-gestao', 'ordem': 3})

        servicos = [
            (cat_proj, 'Projetos de Subestações', 'projetos-subestacoes', 'Subestações 13,8kV a 230kV', 'Projetos completos incluindo arranjo físico, unifilares, aterramento, proteção e controle.'),
            (cat_proj, 'Linhas de Transmissão', 'linhas-transmissao', 'Projetos de LTs até 230kV', 'Projetos com PLS-CADD e levantamento topográfico próprio.'),
            (cat_proj, 'Redes de Distribuição MT/BT', 'redes-distribuicao', 'Redes aéreas e subterrâneas', 'Projetos para concessionárias e consumidores industriais.'),
            (cat_proj, 'Iluminação Pública', 'iluminacao-publica', 'Projetos de iluminação viária', 'Conforme normas ABNT e padrões das concessionárias.'),
            (cat_proj, 'SPDA e Aterramento', 'spda-aterramento', 'Proteção contra descargas atmosféricas', 'Conforme NBR 5419.'),
            (cat_est, 'Fluxo de Potência', 'fluxo-potencia', 'Análise com ETAP', 'Dimensionamento e verificação de sistemas elétricos.'),
            (cat_est, 'Curto-Circuito', 'curto-circuito', 'Correntes de curto-circuito', 'Para seleção de equipamentos e ajuste de proteções.'),
            (cat_est, 'Coordenação de Isolamento', 'coordenacao-isolamento', 'Para subestações e LTs', 'Estudos completos de coordenação.'),
            (cat_exec, 'Gerenciamento PMBOK', 'gerenciamento-pmbok', 'Gestão completa de projetos', 'Do termo de abertura ao encerramento com sistema BK.'),
            (cat_exec, 'Fiscalização de Obras', 'fiscalizacao-obras', 'Acompanhamento técnico', 'Relatórios de conformidade e documentação técnica.'),
            (cat_exec, 'Comissionamento', 'comissionamento', 'Testes e comissionamento', 'Subestações, proteção e instalações industriais.'),
        ]
        for cat, nome, slug, desc_c, desc in servicos:
            Servico.objects.get_or_create(slug=slug, defaults={'categoria': cat, 'nome': nome, 'descricao_curta': desc_c, 'descricao': desc, 'ativo': True})

        for nome, slug in [('Subestações', 'subestacoes'), ('Linhas de Transmissão', 'lts'), ('Prediais/Industriais', 'prediais')]:
            CategoriaPortfolio.objects.get_or_create(slug=slug, defaults={'nome': nome})

        for nome, slug, tipo in [('Equipamentos', 'equipamentos', 'produto'), ('Materiais', 'materiais', 'produto'), ('Softwares BK', 'softwares-bk', 'software')]:
            CategoriaLoja.objects.get_or_create(slug=slug, defaults={'nome': nome, 'tipo': tipo, 'ativo': True})

        self.stdout.write(self.style.SUCCESS('Dados iniciais criados!'))
