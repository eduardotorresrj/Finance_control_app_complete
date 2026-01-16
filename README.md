Finance Control App 📊
A comprehensive personal finance management web application built with Flask. Track your income, expenses, generate reports, and analyze your financial habits with beautiful visualizations.

🌟 Features
💰 Transaction Management: Add, edit, and delete income/expense transactions

📊 Dashboard: Overview of your financial status with interactive charts

📈 Analytics: Monthly comparisons, category breakdowns, and payment method analysis

📄 Reports: Generate detailed monthly reports in PDF format

🔐 User Authentication: Secure login and registration system

📱 Responsive Design: Works perfectly on desktop, tablet, and mobile devices

🎨 Modern UI: Clean Bootstrap 5 interface with dark mode support

🚀 Quick Start
Prerequisites
Python 3.8+

MySQL or SQLite

Git

Installation
Clone the repository

bash
git clone https://github.com/yourusername/finance-control-app.git
cd finance-control-app
Create and activate virtual environment

bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Configure environment variables

bash
cp .env.example .env
# Edit .env with your configuration
Set up the database

sql
-- Create MySQL database (if using MySQL)
CREATE DATABASE finance_control;
Update SQLALCHEMY_DATABASE_URI in your .env file:

env
SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@localhost/finance_control
# or for SQLite:
# SQLALCHEMY_DATABASE_URI=sqlite:///finance.db
Initialize the database

bash
python
>>> from app import db, create_app
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
...     print("Database created!")
Run the application

bash
python app.py
# or for development:
python run.py
Access the application
Open your browser and navigate to: http://localhost:5000

📁 Project Structure
text
finance-control-app/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── Procfile              # Production process file
├── runtime.txt           # Python version specification
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── static/              # Static assets (CSS, JS, images)
│   ├── css/
│   └── js/
├── templates/           # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── analytics.html
│   └── ...
├── models.py           # Database models
├── forms.py            # WTForms definitions
└── routes.py           # Application routes
⚙️ Configuration
Environment Variables
me passe tudo em portugues
Finance Control App 📊
Um aplicativo web completo de gestão financeira pessoal construído com Flask. Acompanhe suas receitas, despesas, gere relatórios e analise seus hábitos financeiros com visualizações bonitas.

🌟 Funcionalidades
💰 Gestão de Transações: Adicionar, editar e excluir transações de receitas/despesas

📊 Dashboard: Visão geral do seu status financeiro com gráficos interativos

📈 Análises: Comparações mensais, distribuição por categorias e análise de métodos de pagamento

📄 Relatórios: Geração de relatórios mensais detalhados em formato PDF

🔐 Autenticação de Usuário: Sistema seguro de login e registro

📱 Design Responsivo: Funciona perfeitamente em desktop, tablet e dispositivos móveis

🎨 Interface Moderna: Interface limpa com Bootstrap 5 e suporte a modo escuro

🚀 Começo Rápido
Pré-requisitos
Python 3.8+

MySQL ou SQLite

Git

Instalação
Clone o repositório

bash
git clone https://github.com/seuusuario/finance-control-app.git
cd finance-control-app
Crie e ative o ambiente virtual

bash
python -m venv venv

# No Windows:
venv\Scripts\activate

# No Mac/Linux:
source venv/bin/activate
Instale as dependências

bash
pip install -r requirements.txt
Configure as variáveis de ambiente

bash
cp .env.example .env
# Edite o arquivo .env com sua configuração
Configure o banco de dados

sql
-- Crie o banco de dados MySQL (se for usar MySQL)
CREATE DATABASE finance_control;
Atualize SQLALCHEMY_DATABASE_URI no seu arquivo .env:

env
SQLALCHEMY_DATABASE_URI=mysql+pymysql://usuario:senha@localhost/finance_control
# ou para SQLite:
# SQLALCHEMY_DATABASE_URI=sqlite:///finance.db
Inicialize o banco de dados

bash
python
>>> from app import db, create_app
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
...     print("Banco de dados criado!")
Execute a aplicação

bash
python app.py
# ou para desenvolvimento:
python run.py
Acesse a aplicação
Abra seu navegador e navegue para: http://localhost:5000

📁 Estrutura do Projeto
text
finance-control-app/
├── app.py                 # Arquivo principal da aplicação
├── requirements.txt       # Dependências Python
├── Procfile              # Arquivo de processos para produção
├── runtime.txt           # Especificação da versão Python
├── .env.example          # Template de variáveis de ambiente
├── .gitignore           # Regras de ignore do Git
├── static/              # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   └── js/
├── templates/           # Templates HTML
│   ├── base.html
│   ├── dashboard.html
│   ├── analytics.html
│   └── ...
├── models.py           # Modelos do banco de dados
├── forms.py            # Definições WTForms
└── routes.py           # Rotas da aplicação
⚙️ Configuração
Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto com base no .env.example:

env
# Configurações de Segurança
SECRET_KEY=sua-chave-secreta-aqui-32-caracteres

# Configurações do Banco de Dados
SQLALCHEMY_DATABASE_URI=sqlite:///finance.db
# SQLALCHEMY_DATABASE_URI=mysql+pymysql://usuario:senha@localhost/finance_control

# Configurações da Aplicação
DEBUG=True
Usando SQLite (Padrão)
A aplicação vem configurada para usar SQLite por padrão. O arquivo do banco será criado automaticamente na primeira execução.

Usando MySQL
Instale o conector MySQL:

bash
pip install pymysql
Atualize a URI de conexão no .env:

env
SQLALCHEMY_DATABASE_URI=mysql+pymysql://usuario:senha@localhost/finance_control
🚀 Implantação
PythonAnywhere (Gratuito)
Crie uma conta em pythonanywhere.com

No Console Bash:

bash
git clone https://github.com/seuusuario/finance-control-app.git
cd finance-control-app
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configure a aplicação web na aba "Web" do dashboard

Configure os arquivos estáticos

Clique em "Reload" para publicar

Render.com (Recomendado para Produção)
https://render.com/images/deploy-to-render-button.svg

📱 Uso da Aplicação
Primeiro Acesso
Acesse http://localhost:5000

Registre uma nova conta

Faça login com suas credenciais

Adicionando Transações
Clique em "Nova Transação" no menu

Selecione o tipo (Receita/Despesa)

Preencha categoria, valor, data e descrição

Clique em "Salvar"

Visualizando Análises
Navegue até "Análises" no menu

Veja gráficos de:

Comparação mensal

Gastos por categoria

Métodos de pagamento

Tabela de resumo mensal

Gerando Relatórios
Acesse "Relatórios" no menu

Clique em "Baixar Relatório" para gerar PDF do mês atual

🛠️ Comandos Úteis
bash
# Criar migrações de banco de dados
flask db init
flask db migrate -m "Mensagem descritiva"
flask db upgrade

# Executar testes
python -m pytest tests/

# Verificar cobertura de código
coverage run -m pytest
coverage report
📊 Tecnologias Utilizadas
Backend: Flask, SQLAlchemy, Flask-Login

Frontend: Bootstrap 5, Chart.js, JavaScript

Banco de Dados: SQLite/MySQL

PDF Generation: xhtml2pdf, ReportLab

Deployment: Gunicorn, PythonAnywhere/Render

🔧 Solução de Problemas
Problemas Comuns
"ModuleNotFoundError: No module named 'pymysql'"

bash
pip install pymysql
Erro de banco de dados

bash
# Recrie o banco de dados
rm finance.db  # Cuidado: apaga todos os dados!
python
>>> from app import db, create_app
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
CSS/JS não carregam

Verifique o console do navegador

Confirme que os arquivos estáticos estão na pasta static/

Reinicie o servidor Flask

Erro ao gerar PDF

Instale as dependências do ReportLab corretamente

Verifique permissões de escrita

📈 Roadmap Futuro
Integração com bancos via API

Orçamentos mensais

Alertas de gastos excessivos

Exportação para Excel

Gráficos de metas financeiras

App móvel nativo

🤝 Contribuindo
Faça um Fork do projeto

Crie uma Branch para sua feature (git checkout -b feature/AmazingFeature)

Commit suas mudanças (git commit -m 'Add some AmazingFeature')

Push para a Branch (git push origin feature/AmazingFeature)

Abra um Pull Request

📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

👨‍💻 Autor
Carlos Eduardo Torres - @eduardotorresrj

🙏 Agradecimentos
Flask - O framework web usado

Bootstrap - Framework CSS

Chart.js - Biblioteca de gráficos

PythonAnywhere - Hospedagem gratuita

📞 Suporte
Encontrou um problema ou tem uma sugestão?

Abra uma Issue

Envie um email para: eduardotorresrj27@gmail.com

⭐ Se este projeto ajudou você, dê uma estrela no GitHub! ⭐
