# 🤖 Discord Bot 24/7 - Bloqueio Automático de Canal

## 📌 Descrição
Este bot foi desenvolvido para **gerenciar o acesso a um canal específico do Discord**.  
Ele controla automaticamente quem pode enviar mensagens em determinados horários, além de oferecer comandos manuais de administração.

### 🔑 Funcionalidades
- ⏰ **Bloqueio automático**:  
  - Todos os usuários são bloqueados das **10h às 19h**, exceto os autorizados.  
- ⏳ **Desbloqueio automático**:  
  - Todos podem enviar mensagens das **19h às 10h**.  
- 🛠 **Comandos manuais**:  
  - `!bloquear` → bloqueia o canal imediatamente (somente Owner).  
  - `!desbloquear` → libera o canal imediatamente (somente Owner).  
- 📜 **Logs**:  
  - Todas as ações são registradas em `bot.log` e também no terminal.  
- 🔁 **Execução 24/7**:  
  - Configurado para rodar em background via `systemd`, reinicia automaticamente após reboot da VPS/Servidor Linux.  

---

## ⚙️ Instalação

### 1️⃣ Clonar repositório
```bash
git clone https://github.com/SEU_USUARIO/discord-bot.git
cd discord-bot
```

### 2️⃣ Criar ambiente virtual (opcional, mas recomendado)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

> O `requirements.txt` deve conter:  
```
discord.py
```

---

## 🔧 Configuração

Edite o arquivo Python (`bot.py`) e configure suas credenciais:

```python
TOKEN = "SEU_TOKEN_DO_DISCORD"
GUILD_ID = 123456789   # ID do servidor
CHANNEL_ID = 987654321 # ID do canal
OWNER_ID = 111111111   # ID do dono do servidor
USER_ID = 222222222    # ID de outro usuário autorizado
```

📌 Para obter os IDs, ative o **Modo Desenvolvedor** no Discord:  
- Configurações → Avançado → Modo Desenvolvedor.  
- Clique com o botão direito em servidor/canal/usuário → "Copiar ID".  

---

## 🚀 Executando o Bot

### Rodando manualmente
```bash
python bot.py
```

### Rodando como serviço (systemd)
Crie o arquivo `/etc/systemd/system/discordbot.service`:

```ini
[Unit]
Description=Discord Bot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/discord-bot
ExecStart=/usr/bin/python3 /home/ubuntu/discord-bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Ativar o serviço:
```bash
sudo systemctl daemon-reload
sudo systemctl enable discordbot
sudo systemctl start discordbot
```

Ver status:
```bash
sudo systemctl status discordbot
```

---

## 🛡 Checklist de Funcionamento
- ✅ Serviço ativo (`systemctl status discordbot`).  
- ✅ Logs visíveis (`journalctl -u discordbot -f`).  
- ✅ Comandos `!bloquear` e `!desbloquear` funcionando.  
- ✅ Canal bloqueia automaticamente às 10h.  
- ✅ Canal desbloqueia automaticamente às 19h.  

---

## ❓ FAQ / Problemas Comuns

**1. O bot não inicia.**  
- Verifique se o TOKEN foi inserido corretamente.  
- Confira se as dependências foram instaladas.  

**2. O bot não bloqueia o canal.**  
- Confirme se o `CHANNEL_ID` está correto.  
- Veja se o bot tem permissões de **Gerenciar Permissões** no canal.  

**3. Quero rodar em outro fuso horário.**  
- Ajuste a VPS/Servidor Linux:  
```bash
sudo timedatectl set-timezone America/Sao_Paulo
```

---

## 📜 Licença
Este projeto é distribuído sob a licença **MIT**.  
Sinta-se livre para usar, modificar e compartilhar.  
