from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.loja.models import Software, CategoriaLoja


class Command(BaseCommand):
    help = 'Cadastra os softwares da BK Engenharia na loja'

    def handle(self, *args, **options):

        # Garante que existe a categoria
        categoria, _ = CategoriaLoja.objects.get_or_create(
            slug='softwares-tecnicos',
            defaults={
                'nome': 'Softwares Técnicos',
                'tipo': 'software',
                'descricao': 'Ferramentas técnicas desenvolvidas pela BK Engenharia'
            }
        )

        # ── SOFTWARE 1: Planejamento Estratégico ─────────────────────────────
        pe_slug = slugify('BK Planejamento Estratégico Empresarial')
        if not Software.objects.filter(slug=pe_slug).exists():
            Software.objects.create(
                categoria=categoria,
                nome='BK Planejamento Estratégico Empresarial',
                slug=pe_slug,
                tagline='Gerencie metas, KPIs e resultados da sua empresa em um único painel.',
                descricao=(
                    'O BK Planejamento Estratégico Empresarial é uma plataforma desenvolvida pela BK Engenharia '
                    'para transformar a gestão estratégica de pequenas e médias empresas. '
                    'Com ele, você define objetivos, acompanha indicadores-chave de desempenho (KPIs), '
                    'monitora metas por área e toma decisões baseadas em dados reais — não em intuição.\n\n'
                    '⚠️ Modelo de contratação obrigatório:\n'
                    '• Implantação: R$ 1.000,00 — configuração completa, personalização e treinamento\n'
                    '• Manutenção mensal: R$ 35,00 — suporte técnico, atualizações e melhorias contínuas\n\n'
                    'Não existe contratação sem manutenção mensal. O modelo garante que você sempre '
                    'terá suporte e a ferramenta sempre atualizada.'
                ),
                funcionalidades=(
                    'Painel de KPIs em tempo real\n'
                    'Balanced Scorecard integrado\n'
                    'Metas por área e colaborador\n'
                    'Análise crítica da direção (compatível ISO 9001)\n'
                    'PDCA automatizado\n'
                    'Relatórios exportáveis em PDF\n'
                    'Acesso via navegador — sem instalação\n'
                    'Suporte técnico incluso na manutenção mensal\n'
                    'Atualizações contínuas inclusas'
                ),
                preco_vitalicio=1000.00,   # implantação
                preco_mensal=35.00,        # manutenção mensal obrigatória
                preco_anual=None,
                imagem_capa='',
                ativo=True,
                destaque=True,
            )
            self.stdout.write(self.style.SUCCESS('✔ BK Planejamento Estratégico cadastrado.'))
        else:
            self.stdout.write(self.style.WARNING('⚠ BK Planejamento Estratégico já existe — ignorado.'))

        # ── SOFTWARE 2: BK Malha de Terra Pro ───────────────────────────────
        mt_pro_slug = slugify('BK Malha de Terra Pro')
        if not Software.objects.filter(slug=mt_pro_slug).exists():
            Software.objects.create(
                categoria=categoria,
                nome='BK Malha de Terra Pro',
                slug=mt_pro_slug,
                tagline='Cálculo automatizado de malha de terra para subestações — IEEE 80 e NBR 5419.',
                descricao=(
                    'O BK Malha de Terra Pro é a versão profissional da plataforma de cálculo de aterramento '
                    'desenvolvida pela BK Engenharia. Ideal para escritórios de engenharia e projetistas '
                    'que precisam de velocidade, precisão e memoriais de cálculo prontos para entrega.\n\n'
                    'O que antes consumia 8 horas de trabalho manual agora é concluído em menos de 30 minutos, '
                    'com memorial de cálculo formatado conforme ABNT, pronto para aprovação em concessionárias.\n\n'
                    '⚠️ Modelo de contratação obrigatório:\n'
                    '• Implantação: R$ 3.500,00 — configuração, treinamento e licença Pro\n'
                    '• Manutenção mensal: R$ 200,00 — suporte técnico, atualizações e melhorias\n\n'
                    'Não existe contratação sem manutenção mensal. O modelo garante suporte contínuo '
                    'e conformidade permanente com as normas IEEE 80 e NBR 5419.'
                ),
                funcionalidades=(
                    'Cálculo de resistência de aterramento (IEEE 80 / NBR 5419)\n'
                    'Memorial de cálculo automático em formato ABNT\n'
                    'Dimensionamento de condutores e eletrodos\n'
                    'Verificação de tensões de passo e toque\n'
                    'Relatório técnico exportável em PDF\n'
                    'Suporte a solos em camadas\n'
                    'Até 10 projetos simultâneos\n'
                    'Suporte técnico incluso na manutenção mensal'
                ),
                preco_vitalicio=3500.00,   # implantação Pro
                preco_mensal=200.00,       # manutenção mensal obrigatória
                preco_anual=None,
                imagem_capa='',
                ativo=True,
                destaque=True,
            )
            self.stdout.write(self.style.SUCCESS('✔ BK Malha de Terra Pro cadastrado.'))
        else:
            self.stdout.write(self.style.WARNING('⚠ BK Malha de Terra Pro já existe — ignorado.'))

        # ── SOFTWARE 3: BK Malha de Terra Enterprise ─────────────────────────
        mt_ent_slug = slugify('BK Malha de Terra Enterprise')
        if not Software.objects.filter(slug=mt_ent_slug).exists():
            Software.objects.create(
                categoria=categoria,
                nome='BK Malha de Terra Enterprise',
                slug=mt_ent_slug,
                tagline='A solução corporativa de aterramento para concessionárias, EPCs e grandes escritórios.',
                descricao=(
                    'O BK Malha de Terra Enterprise é a versão corporativa da plataforma, desenvolvida para '
                    'concessionárias, EPCs e escritórios que gerenciam múltiplos projetos simultaneamente '
                    'e precisam de rastreabilidade, multiusuário e integração com fluxos de aprovação.\n\n'
                    'Inclui tudo do plano Pro, com recursos avançados de gestão, usuários ilimitados, '
                    'histórico de revisões e SLA de suporte prioritário.\n\n'
                    '⚠️ Modelo de contratação obrigatório:\n'
                    '• Implantação: R$ 10.000,00 — configuração corporativa, treinamento de equipe e licença Enterprise\n'
                    '• Manutenção mensal: R$ 200,00 — suporte prioritário, atualizações e SLA garantido\n\n'
                    'Não existe contratação sem manutenção mensal. O modelo garante que sua equipe '
                    'sempre terá suporte técnico especializado e a ferramenta atualizada.'
                ),
                funcionalidades=(
                    'Tudo do plano Pro\n'
                    'Usuários ilimitados\n'
                    'Projetos ilimitados\n'
                    'Histórico de revisões e controle de versões\n'
                    'Fluxo de aprovação com assinaturas digitais\n'
                    'Integração com sistemas de gestão (ERP)\n'
                    'Relatórios consolidados por carteira de projetos\n'
                    'SLA de suporte com resposta em até 4 horas\n'
                    'Treinamento presencial ou remoto incluso na implantação'
                ),
                preco_vitalicio=10000.00,  # implantação Enterprise
                preco_mensal=200.00,       # manutenção mensal obrigatória
                preco_anual=None,
                imagem_capa='',
                ativo=True,
                destaque=True,
            )
            self.stdout.write(self.style.SUCCESS('✔ BK Malha de Terra Enterprise cadastrado.'))
        else:
            self.stdout.write(self.style.WARNING('⚠ BK Malha de Terra Enterprise já existe — ignorado.'))

        self.stdout.write(self.style.SUCCESS('\n✅ Softwares cadastrados com sucesso na loja BK Engenharia.'))
