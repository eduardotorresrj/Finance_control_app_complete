from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    name = StringField('Nome', validators=[Length(max=64)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Repita a senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email já cadastrado.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Solicitar redefinição')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Repita a senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Redefinir senha')

class TransactionForm(FlaskForm):
    type = SelectField('Tipo', choices=[('income','Receita'), ('expense','Despesa')], validators=[DataRequired()])
    category = SelectField('Categoria', choices=[
        ('Luz', '💡 Luz'),
        ('Água', '💧 Água'),
        ('Aluguel', '🏠 Aluguel'),
        ('Condomínio', '🏢 Condomínio'),
        ('Internet', '🌐 Internet'),
        ('Telefone', '📱 Telefone'),
        ('Mercado', '🛒 Mercado'),
        ('Farmácia', '💊 Farmácia'),
        ('Combustível', '⛽ Combustível'),
        ('Educação', '📚 Educação'),
        ('Lazer', '🎮 Lazer'),
        ('Saúde', '🏥 Saúde'),
        ('Transporte', '🚗 Transporte'),
        ('Outros', '📦 Outros'),
        ('Salário', '💰 Salário'),
        ('Freelance', '💼 Freelance'),
        ('Investimentos', '📈 Investimentos'),
        ('Outras Receitas', '💵 Outras Receitas')
    ], validators=[DataRequired()])
    custom_category = StringField('Nova Categoria (se necessário)', validators=[Length(max=64)])
    amount = FloatField('Valor', validators=[DataRequired()])
    date = DateField('Data', validators=[DataRequired()])
    description = TextAreaField('Descrição', validators=[Length(max=200)])
    payment_method = SelectField('Forma de Pagamento', choices=[
        ('', 'Selecione...'),
        ('dinheiro', '💵 Dinheiro'),
        ('debito', '💳 Débito'),
        ('credito', '💳 Crédito'),
        ('pix', '📱 PIX'),
        ('cartao_alimentacao', '🍽️ Cartão Alimentação')
    ])
    submit = SubmitField('Salvar Transação')
