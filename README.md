# BK Engenharia e Tecnologia — Site Oficial

## Instalação local

```bash
# 1. Criar ambiente virtual
python3.13 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env
# Edite .env com seus dados reais

# 4. Banco de dados
python manage.py migrate
python manage.py createsuperuser

# 5. Dados iniciais (categorias e serviços)
python manage.py seed_data

# 6. Rodar servidor
python manage.py runserver
```

## Deploy no Railway

1. Push no GitHub
2. Conectar repositório no Railway
3. Adicionar as variáveis de `.env.example` no painel do Railway
4. Deploy automático

## Estrutura

```
apps/
├── core/           Página inicial, sobre, missão/visão
├── servicos/       Catálogo de serviços
├── portfolio/      Projetos realizados
├── loja/           E-commerce: produtos + softwares
├── blog/           Artigos técnicos (SEO)
├── contato/        Formulário de contato
└── accounts/       Área do cliente com login
```

## Admin Django

Acesse `/admin/` para cadastrar:
- Projetos e categorias de portfólio
- Serviços por categoria
- Produtos e softwares na loja
- Artigos do blog
- Números/KPIs da home

## SEO

O site inclui automaticamente:
- Meta tags em todas as páginas
- Open Graph (Facebook/LinkedIn)
- Schema.org LocalBusiness + EngineeringFirm
- Sitemap automático (`/sitemap.xml`)
- Robots.txt otimizado
- URLs semânticas
