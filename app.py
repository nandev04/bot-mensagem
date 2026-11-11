"""
Retirada automática de senha - Telegram (userbot com Telethon)

Teste: python app.py --now  (envia imediatamente)
"""
import asyncio
import logging
import sys

import config
from bot import executar
from configuracao import configurar

logging.getLogger("telethon").setLevel(logging.ERROR)  # esconde avisos técnicos de conexão


async def main() -> None:
    print("==============================================")
    print("   Retirada automática de senha - Telegram")
    print("   NÃO feche esta janela até a mensagem enviar")
    print("==============================================")

    c = config.carregar() or await configurar()

    mensagem = ""
    while not mensagem:
        mensagem = input("\nDigite a mensagem a enviar: ").strip()
        if not mensagem:
            print("A mensagem não pode ficar em branco.")
    print(f"Mensagem definida: {mensagem}\n")

    await executar(c, mensagem, enviar_agora="--now" in sys.argv)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\nERRO: {e}")
        input("\nPressione Enter para fechar")
        sys.exit(1)
