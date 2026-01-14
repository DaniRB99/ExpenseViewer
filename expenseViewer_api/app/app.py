from app.transactions import create_app
from config import default

def load_config():
    default.loadLoggerConfig()

#LANZAR
# flask --app app.app run --debug --port 8000
if __name__ == "__main__":
    load_config()
    create_app()