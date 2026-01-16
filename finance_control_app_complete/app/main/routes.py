from calendar import calendar
from collections import defaultdict
import traceback
from flask import Blueprint, render_template, redirect, url_for, flash, request, make_response
from app.forms import TransactionForm
from app.models import Transaction
from app import db
from flask_login import login_required, current_user
from datetime import date, datetime, timedelta
import json
# Desabilitar PDF temporariamente para evitar problemas no exe
from xhtml2pdf import pisa
from io import BytesIO

bp = Blueprint('main', __name__, template_folder='templates/main')


# Página inicial
@bp.route('/')
def index():
    return render_template('index.html')


# Dashboard do usuário autenticado
@bp.route('/dashboard')
@login_required
def dashboard():
    today = date.today()
    start = date(today.year, today.month, 1)

    # Busca transações
    txs = current_user.transactions.order_by(Transaction.date.desc()).limit(100).all()
    month_txs = current_user.transactions.filter(Transaction.date >= start).all()

    # Cálculos simplificados sem cartão alimentação
    total_income = sum(t.amount for t in month_txs if t.type == 'income')
    total_expenses = sum(t.amount for t in month_txs if t.type == 'expense')

    # Prepara dados para o gráfico
    transactions_data = []
    for t in month_txs:
        label = f"{t.date.strftime('%d/%m')} - {t.category[:15]}"
        transactions_data.append({
            'label': label,
            'amount': t.amount,
            'type': t.type,
            'date': t.date.strftime('%d/%m/%Y')
        })

    transactions_data.sort(key=lambda x: x['date'])
    labels = [t['label'] for t in transactions_data]
    incomes = [t['amount'] if t['type'] == 'income' else 0 for t in transactions_data]
    expenses = [t['amount'] if t['type'] == 'expense' else 0 for t in transactions_data]

    return render_template('dashboard.html',
                           transactions=txs,
                           labels=json.dumps(labels),
                           incomes=json.dumps(incomes),
                           expenses=json.dumps(expenses),
                           total_income=total_income,
                           total_expenses=total_expenses)


# Adicionar transação
@bp.route('/transaction/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        try:
            category = form.custom_category.data if form.custom_category.data else form.category.data
            tx = Transaction(
                user_id=current_user.id,
                type=form.type.data,
                category=category,
                amount=form.amount.data,
                date=form.date.data,
                description=form.description.data,
                payment_method=form.payment_method.data
            )
            db.session.add(tx)
            db.session.commit()
            flash('Transação adicionada com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao adicionar a transação: {str(e)}', 'danger')
    elif request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'danger')
    return render_template('add_transaction.html', form=form)


# Relatórios --------------------------------------------
@bp.route('/reports')
@login_required
def reports():
    try:
        today = date.today()
        start = date(today.year, today.month, 1)
        end = date(today.year, today.month, 31)
        txs = current_user.transactions.filter(Transaction.date >= start, Transaction.date <= end).all()
        total_income = sum(t.amount for t in txs if t.type == 'income')
        total_expenses = sum(t.amount for t in txs if t.type == 'expense')

        return render_template('reports.html',
                               transactions=txs,
                               total_income=total_income,
                               total_expenses=total_expenses)
    except Exception as e:
        flash(f'Erro ao gerar relatório: {str(e)}', 'danger')
        return redirect(url_for('main.dashboard'))


# Editar transação
@bp.route('/transaction/edit/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        flash('Você não tem permissão para editar esta transação.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = TransactionForm(obj=transaction)
    if form.validate_on_submit():
        category = form.custom_category.data if form.custom_category.data else form.category.data
        transaction.type = form.type.data
        transaction.category = category
        transaction.amount = form.amount.data
        transaction.date = form.date.data
        transaction.description = form.description.data
        transaction.payment_method = form.payment_method.data
        db.session.commit()
        flash('Transação atualizada com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('edit_transaction.html', form=form, transaction=transaction)


# Excluir transação
@bp.route('/transaction/delete/<int:transaction_id>')
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        flash('Você não tem permissão para excluir esta transação.', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.delete(transaction)
    db.session.commit()
    flash('Transação excluída com sucesso!', 'success')
    return redirect(url_for('main.dashboard'))


# Analytics --------------------------------------------
@bp.route('/analytics')
@login_required
def analytics():
    from collections import defaultdict
    from datetime import timedelta

    try:
        print("=== INICIANDO ANALYTICS ===")

        # Dados mensais
        months_data = []
        months_labels = []
        today = date.today()

        print(f"Data atual: {today}")

        # Gerar os últimos 6 meses (do mais antigo para o mais recente)
        for i in range(5, -1, -1):  # 5, 4, 3, 2, 1, 0
            # Calcular mês i meses atrás
            year = today.year
            month = today.month - i

            # Ajustar se o mês for menor que 1
            while month < 1:
                month += 12
                year -= 1

            # Primeiro dia do mês
            month_start = date(year, month, 1)

            # Último dia do mês (abordagem segura)
            if month == 12:
                month_end = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                month_end = date(year, month + 1, 1) - timedelta(days=1)

            print(f"Mês {i}: {month_start.strftime('%m/%Y')} ({month_start} a {month_end})")

            # Buscar transações do mês
            month_txs = current_user.transactions.filter(
                Transaction.date >= month_start,
                Transaction.date <= month_end
            ).all()

            print(f"  Transações encontradas: {len(month_txs)}")

            # Calcular totais
            income = sum(t.amount for t in month_txs if t.type == 'income')
            expenses = sum(t.amount for t in month_txs if t.type == 'expense')
            balance = income - expenses

            months_data.append({
                'income': float(income),
                'expense': float(expenses),
                'balance': float(balance)
            })
            months_labels.append(month_start.strftime('%m/%Y'))

        print(f"\nDados mensais: {len(months_data)} meses")

        # Categorias de gastos (últimos 3 meses)
        three_months_ago = today - timedelta(days=90)
        print(f"Últimos 3 meses desde: {three_months_ago}")

        recent_txs = current_user.transactions.filter(
            Transaction.date >= three_months_ago
        ).all()

        print(f"Transações últimos 3 meses: {len(recent_txs)}")

        # Agrupar despesas por categoria
        category_expenses = {}
        for t in recent_txs:
            if t.type == 'expense':
                cat = t.category or 'Sem categoria'
                category_expenses[cat] = category_expenses.get(cat, 0) + float(t.amount)

        # Ordenar e pegar top 10
        top_categories = sorted(
            category_expenses.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        print(f"Top categorias encontradas: {len(top_categories)}")

        # Métodos de pagamento
        payment_methods_data = {}
        for t in recent_txs:
            if t.type == 'expense' and t.payment_method:
                method = t.payment_method
                payment_methods_data[method] = payment_methods_data.get(method, 0) + float(t.amount)

        payment_methods = sorted(
            payment_methods_data.items(),
            key=lambda x: x[1],
            reverse=True
        )

        print(f"Métodos de pagamento: {len(payment_methods)}")
        print("=== FIM ANALYTICS ===\n")

        return render_template('analytics.html',
                               months_data=months_data,
                               months_labels=months_labels,
                               top_categories=top_categories,
                               payment_methods=payment_methods)

    except Exception as e:
        print(f"ERRO EM ANALYTICS: {str(e)}")
        import traceback
        print(traceback.format_exc())

        # Retornar dados vazios em caso de erro
        return render_template('analytics.html',
                               months_data=[],
                               months_labels=[],
                               top_categories=[],
                               payment_methods=[])


# Página de perfil do usuário
@bp.route('/profile')
@login_required
def profile():
    from datetime import timedelta
    from collections import Counter

    total_transactions = current_user.transactions.count()
    thirty_days_ago = date.today() - timedelta(days=30)
    recent_txs = current_user.transactions.filter(Transaction.date >= thirty_days_ago).all()

    total_income_30d = sum(t.amount for t in recent_txs if t.type == 'income')
    total_expense_30d = sum(t.amount for t in recent_txs if t.type == 'expense')

    categories = Counter([t.category for t in current_user.transactions.all()])
    top_categories = categories.most_common(5)

    return render_template('profile.html',
                           user=current_user,
                           total_transactions=total_transactions,
                           total_income_30d=total_income_30d,
                           total_expense_30d=total_expense_30d,
                           top_categories=top_categories)


@bp.route('/reports/download')
@login_required
def reports_download():
    try:
        print("DEBUG: Iniciando geração de relatório PDF...")

        # Obter dados do mês atual - SEM calendar.monthrange
        today = date.today()
        start = date(today.year, today.month, 1)

        # Calcular o último dia do mês de forma segura
        if today.month == 12:
            end = date(today.year + 1, 1, 1)  # Primeiro dia do próximo ano
        else:
            end = date(today.year, today.month + 1, 1)  # Primeiro dia do próximo mês

        # Subtrair 1 dia para obter o último dia do mês atual
        from datetime import timedelta
        end = end - timedelta(days=1)

        print(f"DEBUG: Período do relatório: {start} até {end}")

        # Buscar transações reais
        transactions = current_user.transactions.filter(
            Transaction.date >= start,
            Transaction.date <= end
        ).order_by(Transaction.date).all()

        print(f"DEBUG: {len(transactions)} transações encontradas")

        # Se não houver transações, retornar mensagem
        if not transactions:
            flash('Não há transações para gerar relatório deste mês.', 'warning')
            return redirect(url_for('main.reports'))

        # Calcular totais
        total_income = 0.0
        total_expense = 0.0

        for t in transactions:
            if t.type == 'income':
                total_income += t.amount
            else:
                total_expense += t.amount

        balance = total_income - total_expense

        print(f"DEBUG: Receitas: R$ {total_income:.2f}, Despesas: R$ {total_expense:.2f}")

        # Calcular top categorias de despesas
        category_expenses = {}
        for t in transactions:
            if t.type == 'expense':
                if t.category in category_expenses:
                    category_expenses[t.category] += t.amount
                else:
                    category_expenses[t.category] = t.amount

        # Ordenar e pegar top 5
        top_categories = sorted(category_expenses.items(), key=lambda x: x[1], reverse=True)[:5]

        print(f"DEBUG: Top categorias: {top_categories}")

        # Nome do mês em português
        month_names_pt = [
            'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
            'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
        ]
        month_name = month_names_pt[today.month - 1]

        # Preparar dados para o template
        template_data = {
            'user': current_user,
            'current_date': datetime.now(),
            'month': today.month,
            'year': today.year,
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'top_categories': top_categories,
            'transactions': transactions
        }

        print("DEBUG: Renderizando template...")

        # Renderizar HTML
        html_content = render_template('monthly_report.html', **template_data)

        print("DEBUG: Convertendo para PDF...")

        # Converter para PDF
        pdf_buffer = BytesIO()

        # Converter string para bytes
        html_bytes = html_content.encode('utf-8')

        # Criar PDF
        pisa_status = pisa.CreatePDF(
            src=BytesIO(html_bytes),
            dest=pdf_buffer,
            encoding='utf-8'
        )

        # Verificar se houve erro
        if pisa_status.err:
            error_msg = 'Erro ao criar PDF. Verifique o template HTML.'
            print(f"ERRO PDF: {error_msg}")
            flash(error_msg, 'danger')
            return redirect(url_for('main.reports'))

        pdf_buffer.seek(0)

        # Verificar se o PDF foi gerado
        pdf_size = len(pdf_buffer.getvalue())
        if pdf_size == 0:
            flash('Erro: PDF vazio gerado', 'danger')
            return redirect(url_for('main.reports'))

        print(f"DEBUG: PDF gerado com {pdf_size} bytes")

        # Criar resposta
        filename = f'relatorio_{month_name}_{today.year}.pdf'
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'

        print(f"DEBUG: Relatório '{filename}' enviado com sucesso")
        flash(f'Relatório de {month_name} gerado com sucesso!', 'success')

        return response

    except Exception as e:
        error_msg = f'Erro ao gerar relatório PDF: {str(e)}'
        print(f"ERRO CRÍTICO: {error_msg}")
        print(traceback.format_exc())
        flash(error_msg, 'danger')
        return redirect(url_for('main.reports'))
