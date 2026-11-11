"""Credenciais da API do Telegram, lidas do .env (embutido no .exe no build)."""
import os
import sys

from dotenv import load_dotenv

if getattr(sys, "frozen", False):
    # PyInstaller --onefile extrai os arquivos de --add-data em sys._MEIPASS
    _env_path = os.path.join(sys._MEIPASS, ".env")
else:
    _env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

load_dotenv(_env_path)

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
