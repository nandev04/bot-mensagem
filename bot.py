"""Conexão com o Telegram, envio agendado e escuta da resposta."""
import asyncio
import time
from datetime import timedelta

from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.sessions import StringSession

import config
from credenciais import API_ID, API_HASH
from relogio import agora, fmt, log, proximo_disparo, sincronizar

TENTATIVAS = 60
INTERVALO_TENTATIVA = 2.0  # s
VERIFICACAO = 0.01         # s entre checagens do horário
RESSINCRONIZAR = 600       # s entre sincronizações NTP


async def _conectar(session: str) -> TelegramClient:
    client = TelegramClient(StringSession(session), API_ID, API_HASH,
                            connection_retries=None, auto_reconnect=True)
    await client.connect()
    if not await client.is_user_authorized():
        raise RuntimeError("A sessão do Telegram expirou. Apague o config.json e abra o programa de novo.")
    return client


def _escutar_respostas(client: TelegramClient, target, enviadas: set[int]) -> None:
    # Num grupo chegam mensagens de todo mundo: só interessam respostas
    # à mensagem dela ou mensagens que a mencionam.
    @client.on(events.NewMessage(chats=target, incoming=True))
    async def resposta(ev):
        eh_resposta = ev.message.reply_to_msg_id in enviadas
        if not (eh_resposta or ev.message.mentioned):
            return
        texto = ev.message.message
        log(f"RESPOSTA RECEBIDA:\n\n{texto}\n\a")  # \a = bipe
        config.registrar_resposta(fmt(agora()), texto)


async def _enviar(client: TelegramClient, target, mensagem: str, enviadas: set[int]) -> None:
    for tentativa in range(1, TENTATIVAS + 1):
        try:
            msg = await client.send_message(target, mensagem)
            enviadas.add(msg.id)
            log(f"Mensagem enviada! (tentativa {tentativa}) Aguardando resposta...")
            return
        except FloodWaitError as e:
            espera = e.seconds + 1
            log(f"FloodWait do Telegram (tentativa {tentativa}): aguardar {e.seconds}s. "
                f"Considere aumentar INTERVALO_TENTATIVA.")
            await asyncio.sleep(espera)
        except Exception as e:
            log(f"Falha ao enviar (tentativa {tentativa}): {e}")
            await asyncio.sleep(INTERVALO_TENTATIVA)
    log("Não foi possível enviar após todas as tentativas.")


async def executar(c: config.Config, mensagem: str, enviar_agora: bool = False) -> None:
    await asyncio.to_thread(sincronizar, True)

    client = await _conectar(c["session"])
    # A StringSession não guarda o cache de chats; carregar os diálogos
    # é o que permite resolver o grupo a partir do ID numérico.
    await client.get_dialogs()
    target = await client.get_entity(c["target"])
    log(f"Conectado. Destino: {c['target_nome']}")

    enviadas: set[int] = set()
    _escutar_respostas(client, target, enviadas)

    if enviar_agora:
        await _enviar(client, target, mensagem, enviadas)

    alvo = proximo_disparo(c["weekday"], c["hour"], c["minute"])
    log(f"Próximo envio: {fmt(alvo)}")

    ultima_sync = time.monotonic()
    while True:
        if time.monotonic() - ultima_sync > RESSINCRONIZAR:
            ultima_sync = time.monotonic()
            asyncio.create_task(asyncio.to_thread(sincronizar))
        if agora() >= alvo:
            atual = alvo
            alvo = proximo_disparo(c["weekday"], c["hour"], c["minute"], atual + timedelta(seconds=1))
            await _enviar(client, target, mensagem, enviadas)
        await asyncio.sleep(VERIFICACAO)
