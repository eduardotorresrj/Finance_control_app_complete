from app.models import User, Transaction
from app.email_utils import send_email
from datetime import date
from flask import render_template
from flask_mail import Message
from app import mail
from threading import Thread
from xhtml2pdf import pisa
from io import BytesIO

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email_with_attachment(app, subject, recipient, html_body, pdf_bytes):
    msg = Message(subject, recipients=[recipient])
    msg.html = html_body
    msg.attach('relatorio_mensal.pdf', 'application/pdf', pdf_bytes)
    Thread(target=send_async_email, args=(app, msg)).start()

def generate_pdf_from_html(html_content):
    """Gera PDF a partir do HTML usando xhtml2pdf"""
    pdf_buffer = BytesIO()
    pisa.CreatePDF(html_content, dest=pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

def schedule_monthly_reports(app):
    with app.app_context():
        users = User.query.all()
        for user in users:
            # Pega o mês anterior
            today = date.today()
            year = today.year
            month = today.month - 1 or 12
            if today.month == 1:
                year = today.year - 1
                month = 12
            
            start = date(year, month, 1)
            if month == 12:
                end = date(year+1, 1, 1)
            else:
                end = date(year, month+1, 1)
            
            txs = user.transactions.filter(Transaction.date >= start, Transaction.date < end).all()
            total_income = sum(t.amount for t in txs if t.type == 'income')
            total_expense = sum(t.amount for t in txs if t.type == 'expense')
            balance = total_income - total_expense
            
            # Análise por categoria
            from collections import defaultdict
            category_expenses = defaultdict(float)
            for t in txs:
                if t.type == 'expense':
                    category_expenses[t.category] += t.amount
            
            top_categories = sorted(category_expenses.items(), key=lambda x: x[1], reverse=True)[:5]
            
            try:
                # Gera o HTML do relatório
                html = render_template(
                    'main/monthly_report.html', 
                    user=user, 
                    transactions=txs, 
                    total_income=total_income, 
                    total_expense=total_expense,
                    balance=balance,
                    top_categories=top_categories,
                    month=month,
                    year=year
                )
                
                # Gera o PDF
                pdf_bytes = generate_pdf_from_html(html)
                
                # Envia o email
                subject = f'📊 Relatório Mensal - {month:02d}/{year}'
                send_email_with_attachment(app, subject, user.email, html, pdf_bytes)
                app.logger.info(f'Relatório enviado com sucesso para {user.email}')
                
            except Exception as e:
                app.logger.error(f'Erro ao gerar/enviar relatório para {user.email}: {e}')
