# 📩 Retirada Automática de Senha — Telegram Userbot

> Userbot em Python que envia **mensagens agendadas periodicamente** pela sua própria conta do Telegram e captura a resposta automaticamente.

Feito originalmente para automatizar a retirada semanal de senha de visita num grupo, mas serve para qualquer envio recorrente que dependa da janela de abertura de um grupo (ex.: inscrições, reservas, confirmações).

---

## ✨ Funcionalidades

- 🗓️ **Agendamento semanal** — define dia da semana + horário, dispara sozinho na hora certa.
- 🕒 **Relógio corrigido por NTP** — não depende do relógio do PC estar certo; sincroniza com servidores de tempo da internet.
- 🔁 **Retry resiliente** — tenta reenviar por até 2 minutos caso o grupo ainda esteja fechado, respeitando `FloodWaitError` do Telegram.
- 👂 **Captura automática da resposta** — escuta a resposta à mensagem enviada e salva em `respostas.txt`.
- 🔐 **Mensagem digitada a cada execução** — como medida de segurança, o texto não é fixo nem salvo em disco.
- 🔔 **Bipe ao receber resposta** — alerta sonoro quando a resposta chega.
- 📦 **Distribuído como `.exe`** — um único arquivo, sem precisar instalar Python na máquina da usuária.

---

## 🚀 Como funciona

1. No primeiro uso, pede o telefone e o código do Telegram para autenticar como userbot.
2. Lista seus grupos para você escolher o destino.
3. Pergunta o dia da semana e horário do envio.
4. A cada execução, pede a mensagem a ser enviada (não guarda).
5. Fica rodando em background, sincroniza o horário via NTP, e dispara no momento exato.
6. Se o grupo estiver fechado, retenta por até 2 minutos.
7. Quando a resposta chega, salva em `respostas.txt` e emite um bipe.

---

## 📦 Requisitos

- **Para desenvolver / gerar o `.exe`:** Windows + Python 3.10+
- **Para apenas usar:** Windows (o `.exe` já é auto-contido)

---

## 🛠️ Gerar o `.exe` (desenvolvedor)

1. Instale o **Python 3.10+** (marque *Add Python to PATH*).
2. Crie um app em [my.telegram.org](https://my.telegram.org) → *API development tools*.
3. Copie `.env.example` para `.env` e preencha `API_ID` e `API_HASH`:
   ```env
   API_ID=1234567
   API_HASH=sua_hash_aqui
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. (Opcional) Teste localmente:
   ```bash
   python app.py --now    # configura e envia na hora
   python app.py          # configura e espera o horário agendado
   ```
6. Apague o `config.json` gerado no teste.
7. Rode o build:
   ```bash
   build.bat
   ```
   O executável sai em `dist\RetiradaSenha.exe`. O `.env` fica embutido no binário.

---

## 📥 Uso (usuária final)

1. Coloque `RetiradaSenha.exe` numa pasta própria (ex.: `Documentos\Senha`).
2. **Primeira vez:** clique duas vezes e preencha:
   - 📱 Telefone + código enviado pelo Telegram
   - 💬 Grupo de destino (escolha na lista)
   - 🗓️ Dia e horário do envio

   Fica tudo salvo em `config.json`.
3. **Toda semana:** abra o programa até ~30 minutos antes do horário, **digite a mensagem** a ser enviada e deixe a janela aberta. Ele envia sozinho, apita e mostra a resposta — que também fica em `respostas.txt`.
4. Para mudar a configuração: apague o `config.json` e abra de novo.

---

## ⚙️ Detalhes técnicos

- **Linguagem:** Python 3.10+
- **Biblioteca Telegram:** [Telethon](https://docs.telethon.dev/) (userbot — usa sua conta, não um bot token)
- **Empacotamento:** PyInstaller (`--onefile`)
- **Credenciais:** `.env` embutido via `--add-data` + `python-dotenv`
- **Agendamento:** in-process, sem cron/Task Scheduler
- **Latência típica:** ~10ms para detecção do horário + ping até o Telegram (~100-300ms)

---

## 📁 Estrutura

```
.
├── app.py              # Ponto de entrada: valida config e dispara o bot
├── bot.py              # Conexão Telegram, envio agendado, escuta de respostas
├── configuracao.py     # Setup inicial interativo (telefone, grupo, horário)
├── config.py           # Caminhos + leitura/gravação do config.json
├── credenciais.py      # Loader do .env (API_ID, API_HASH)
├── relogio.py          # Sincronização NTP, cálculo do próximo disparo
├── .env                # Credenciais da API (gitignored)
├── build.bat           # Script de build do .exe
└── requirements.txt
```

---

## ⚠️ Avisos importantes

- 🔒 **O `config.json` contém a sessão da sua conta do Telegram** — equivale a estar logado. **Não compartilhe.**
- 🔒 **O `.env` e o `.exe` embutem suas credenciais da API** — não distribua publicamente.
- 💤 **O PC não pode suspender/hibernar** enquanto o programa espera o horário.
- 🛡️ **SmartScreen / antivírus** podem alertar (é um `.exe` não assinado): *Mais informações → Executar assim mesmo*.
- 📵 **Uso responsável:** é um userbot; respeite os [Termos de Serviço do Telegram](https://telegram.org/tos). Envios em massa ou spam podem resultar em restrições na conta.

---

## 📝 Licença

MIT — use, modifique e compartilhe à vontade.
