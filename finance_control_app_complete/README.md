# Finance Control App

1. Copy files.
2. Create virtualenv and run: pip install -r requirements.txt
3. Configure .env from .env.example
4. Create MySQL DB and update SQLALCHEMY_DATABASE_URI
5. Run: python run.py
6. For production use gunicorn and run scheduler in same process.
