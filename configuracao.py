"""Assistente da primeira execução: login no Telegram e preferências."""
from telethon import TelegramClient
from telethon.sessions import StringSession

import config
from credenciais import API_ID, API_HASH
from relogio import DIAS


def perguntar(texto: str, padrao: str = "") -> str:
    r = input(f"{texto} [{padrao}]: " if padrao else f"{texto}: ").strip()
    return r or padrao


async def _pedir_destino(client: TelegramClient) -> tuple[int, str]:
    """Lista os grupos da conta e devolve (id, nome) do escolhido."""
    grupos = [d async for d in client.iter_dialogs() if d.is_group]
    if not grupos:
        raise RuntimeError("Essa conta não participa de nenhum grupo.")

    print("\nGrupos da sua conta:")
    for i, g in enumerate(grupos, 1):
        print(f"  {i:>2}. {g.name}")

    while True:
        n = perguntar("\nNúmero do grupo da senha")
        if n.isdigit() and 1 <= int(n) <= len(grupos):
            g = grupos[int(n) - 1]
            return g.id, g.name
        print("Número inválido.")


def _pedir_dia() -> int:
    dia = perguntar("Dia da semana", "quinta").lower()[:3]
    return next((i for i, d in enumerate(DIAS) if d.startswith(dia)), DIAS.index("quinta"))


def _pedir_horario() -> tuple[int, int]:
    while True:
        h = perguntar("Horário (HH:MM)", "08:00").replace("h", ":")
        try:
            hour, minute = (int(x) for x in h.split(":"))
            if 0 <= hour < 24 and 0 <= minute < 60:
                return hour, minute
        except ValueError:
            pass
        print("Formato inválido. Use por exemplo 08:00")


async def configurar() -> config.Config:
    print("\n=== Configuração inicial (só na primeira vez) ===\n")
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.start(
        phone=lambda: perguntar("Seu telefone com DDD (ex: +5511999998888)"),
        code_callback=lambda: perguntar("Código que chegou no Telegram"),
        password=lambda: perguntar("Senha de verificação em 2 etapas"),
    )
    try:
        target, target_nome = await _pedir_destino(client)
        weekday = _pedir_dia()
        hour, minute = _pedir_horario()
        c: config.Config = {
            "session": client.session.save(),
            "target": target, "target_nome": target_nome,
            "weekday": weekday, "hour": hour, "minute": minute,
        }
    finally:
        await client.disconnect()

    config.salvar(c)
    print("\nConfiguração salva. Para mudar depois, apague o config.json e abra o programa de novo.\n")
    return c
