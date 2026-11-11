"""Hora corrigida por NTP, fuso de São Paulo e cálculo do próximo envio."""
import socket
import struct
import time
from datetime import datetime, timedelta, timezone

SP = timezone(timedelta(hours=-3))  # America/Sao_Paulo, sem horário de verão desde 2019
DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]  # = datetime.weekday()
SERVIDORES_NTP = ("a.st1.ntp.br", "pool.ntp.org", "time.google.com")

_offset = 0.0  # segundos a somar ao relógio do PC


def _consultar_ntp(host: str) -> float:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(3)
        t0 = time.time()
        s.sendto(b"\x1b" + 47 * b"\0", (host, 123))
        data, _ = s.recvfrom(48)
        t1 = time.time()
    secs, frac = struct.unpack("!II", data[40:48])
    servidor = secs - 2208988800 + frac / 2**32  # NTP conta desde 1900; Unix desde 1970
    return servidor + (t1 - t0) / 2 - t1


def sincronizar(verbose: bool = False) -> None:
    """Bloqueante (até ~9 s): chame via asyncio.to_thread."""
    global _offset
    for host in SERVIDORES_NTP:
        try:
            _offset = _consultar_ntp(host)
            if verbose:
                log(f"Relógio sincronizado (diferença do PC: {_offset:+.1f} s)")
            return
        except OSError:
            continue
    if verbose:
        log("Não foi possível sincronizar pela internet; usando o relógio do computador.")


def agora() -> datetime:
    return datetime.fromtimestamp(time.time() + _offset, SP)


def fmt(dt: datetime) -> str:
    return f"{DIAS[dt.weekday()]} {dt:%d/%m} às {dt:%H:%M:%S}"


def log(msg: str) -> None:
    print(f"[{agora():%H:%M:%S}] {msg}", flush=True)


def proximo_disparo(weekday: int, hour: int, minute: int, ref: datetime | None = None) -> datetime:
    ref = ref or agora()
    dias = (weekday - ref.weekday()) % 7
    alvo = (ref + timedelta(days=dias)).replace(hour=hour, minute=minute, second=0, microsecond=0)
    return alvo if alvo > ref else alvo + timedelta(days=7)
