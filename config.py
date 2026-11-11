"""Caminhos dos arquivos e leitura/gravação do config.json."""
import json
import os
import sys
from typing import TypedDict

# Arquivos ficam ao lado do .exe (ou do app.py, quando roda pelo Python)
if getattr(sys, "frozen", False):
    BASE = os.path.dirname(sys.executable)
else:
    BASE = os.path.dirname(os.path.abspath(__file__))

CONFIG = os.path.join(BASE, "config.json")
RESPOSTAS = os.path.join(BASE, "respostas.txt")


class Config(TypedDict):
    session: str   # sessão do Telegram (equivale ao login)
    target: int       # ID numérico do grupo (ex.: -1001234567890)
    target_nome: str  # nome do grupo, só para exibir
    weekday: int   # 0 = segunda ... 6 = domingo
    hour: int
    minute: int


def carregar() -> Config | None:
    if not os.path.exists(CONFIG):
        return None
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def salvar(c: Config) -> None:
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)


def registrar_resposta(quando: str, texto: str) -> None:
    with open(RESPOSTAS, "a", encoding="utf-8") as f:
        f.write(f"{quando}\n{texto}\n\n")
