import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config

db = SQLAlchemy()
login = LoginManager()
mail = Mail()
scheduler = BackgroundScheduler()

def create_app(base_path=None, config_class=Config):
    """Cria a aplicação Flask com todos os recursos e path ajustado para .exe"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ajuste do banco de dados para .exe
    if base_path:
        db_path = os.path.join(base_path, "financas.db")
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login.init_app(app)
    login.login_view = 'auth.login'
    mail.init_app(app)

    # Importa e registra Blueprints
    from app.auth.routes import bp as auth_bp
    from app.main.routes import bp as main_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    # Agendamento de relatórios mensais
    from app.tasks import schedule_monthly_reports
    scheduler.add_job(func=schedule_monthly_reports, trigger='cron', day='1', hour=6, args=[app])
    scheduler.start()

    # Criação das tabelas no banco
    with app.app_context():
        db.create_all()

    return app
