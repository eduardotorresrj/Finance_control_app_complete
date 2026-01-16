# 📧 Configuração do Envio Automático de Relatórios

## Como Funciona

O sistema envia automaticamente um relatório mensal em PDF para todos os usuários no **dia 1º de cada mês às 6h da manhã**.

## Configuração Necessária

Para que o envio automático funcione, você precisa configurar as variáveis de ambiente de email.

### 1. Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta_aqui
SQLALCHEMY_DATABASE_URI=sqlite:///app.db

# Configurações de Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu_email@gmail.com
MAIL_PASSWORD=sua_senha_de_app
ADMIN_EMAIL=seu_email@gmail.com
```

### 2. Para Gmail:

1. **Ative a verificação em 2 etapas** na sua conta Google
2. **Gere uma senha de app:**
   - Acesse: https://myaccount.google.com/apppasswords
   - Selecione "Aplicativo": Email
   - Selecione "Dispositivo": Outro (digite "Finance Control")
   - Clique em "Gerar"
   - Copie a senha gerada e use no `MAIL_PASSWORD`

### 3. Para Outlook/Hotmail:

```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu_email@outlook.com
MAIL_PASSWORD=sua_senha
```

### 4. Para outros provedores:

Consulte a documentação do seu provedor de email para as configurações SMTP corretas.

## Testando o Envio

Para testar se o envio está funcionando, você pode:

1. **Testar manualmente:**
   ```python
   # No terminal Python
   from app import create_app
   from app.tasks import schedule_monthly_reports
   
   app = create_app()
   schedule_monthly_reports(app)
   ```

2. **Mudar o horário de envio:**
   No arquivo `app/__init__.py`, linha 28, você pode alterar:
   ```python
   scheduler.add_job(func=schedule_monthly_reports, trigger='cron', day='1', hour=6, args=[app])
   ```
   
   Para testar, mude para:
   ```python
   # Enviar todos os dias às 10h (para teste)
   scheduler.add_job(func=schedule_monthly_reports, trigger='cron', hour=10, args=[app])
   ```

## O que é Enviado

Cada usuário recebe um email com:
- ✅ PDF anexado com o relatório completo do mês anterior
- ✅ Resumo financeiro (receitas, despesas, saldo)
- ✅ Top 5 categorias de gastos
- ✅ Lista completa de todas as transações
- ✅ Taxa de economia

## Solução de Problemas

### Email não está sendo enviado:

1. Verifique se as configurações SMTP estão corretas
2. Verifique se o servidor está rodando no dia 1º às 6h
3. Verifique os logs do aplicativo para erros

### Erro de autenticação:

- Para Gmail: Use senha de app, não a senha normal
- Verifique se a verificação em 2 etapas está ativada

### Erro de conexão:

- Verifique se o `MAIL_SERVER` e `MAIL_PORT` estão corretos
- Verifique se o firewall não está bloqueando a conexão SMTP

## Importante

⚠️ **O servidor precisa estar rodando no dia 1º de cada mês às 6h da manhã para enviar os relatórios automaticamente.**

Para produção, considere usar:
- **Heroku Scheduler** (se hospedar no Heroku)
- **Cron Job** (se hospedar em servidor Linux)
- **AWS EventBridge** (se hospedar na AWS)
- **Azure Functions** (se hospedar no Azure)

## Alternativa: Envio Manual

Se preferir enviar manualmente, você pode criar uma rota administrativa:

```python
@bp.route('/admin/send-reports')
@login_required
def send_reports_manual():
    if current_user.email != 'seu_email_admin@email.com':
        flash('Acesso negado', 'danger')
        return redirect('/')
    
    schedule_monthly_reports(current_app)
    flash('Relatórios enviados!', 'success')
    return redirect('/')
```

