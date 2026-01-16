import os
import sys
import time
import threading
import webbrowser
from app import create_app

try:
    # Ajuste do path para banco de dados no .exe
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    # Cria a aplicação Flask passando o base_path
    app = create_app(base_path)

    def open_browser_once():
        """Abre o navegador após o servidor iniciar, apenas uma vez"""
        time.sleep(0.5)
        webbrowser.open('http://127.0.0.1:5000', new=1)

    if __name__ == '__main__':
        threading.Thread(target=open_browser_once, daemon=True).start()
        print("=" * 50)
        print("Finance Control App iniciado com sucesso!")
        print("=" * 50)
        app.run(debug=False, use_reloader=False)

except Exception as e:
    print(f"Erro ao iniciar o aplicativo: {e}")
    import traceback
    traceback.print_exc()
    input("Pressione Enter para sair...")
    sys.exit(1)
