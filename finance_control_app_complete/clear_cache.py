import os
import shutil
from app import create_app

def clear_jinja_cache():
    app = create_app()
    app.jinja_env.cache = {}
    print("✅ Cache interno do Jinja2 limpo com sucesso.")

def remove_pycache_dirs():
    dirs = [
        "__pycache__",
        "instance",
        "app\\__pycache__",
        "app\\main\\__pycache__"
    ]
    for d in dirs:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
                print(f"🗑️  Removido: {d}")
            except Exception as e:
                print(f"Erro ao remover {d}: {e}")
        else:
            print(f"(Ignorado) {d} não encontrado.")

if __name__ == "__main__":
    print("=== Limpando cache do Flask e Jinja2 ===")
    clear_jinja_cache()
    remove_pycache_dirs()
    print("✅ Limpeza concluída. Agora reinicie o servidor com:")
    print("flask run")
