#!/root/discord-bot/venv/bin/python
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands, tasks
from datetime import datetime
import logging

# =========================
# CONFIGURACAO DE LOG
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),  # forca UTF-8
        logging.StreamHandler()
    ]
)

# =========================
# CONFIGURACAO DO BOT
# =========================
TOKEN = "COLOQUE AQUI O TOKEN"

GUILD_ID = ID do servidor
CHANNEL_ID = ID do canal a ser controlado
OWNER_ID = ID do owner do server (autorizado a mandar mensagens quando bloqueado)
USER_ID = ID de outro user (autorizado a mandar mensagens)

canal_bloqueado = False
avisos_enviados = set()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# FUNCOES DE BLOQUEIO/DESBLOQUEIO
# =========================
async def bloquear_canal():
    guild = bot.get_guild(GUILD_ID)
    canal = guild.get_channel(CHANNEL_ID)
    if canal:
        overwrite = discord.PermissionOverwrite(send_messages=False)
        await canal.set_permissions(guild.default_role, overwrite=overwrite)
        dono = guild.get_member(OWNER_ID)
        user = guild.get_member(USER_ID)
        if dono:
            await canal.set_permissions(dono, send_messages=True)
        if user:
            await canal.set_permissions(user, send_messages=True)
        logging.info("🔒 Canal bloqueado para todos, exceto autorizados")
        return True
    return False

async def desbloquear_canal():
    guild = bot.get_guild(GUILD_ID)
    canal = guild.get_channel(CHANNEL_ID)
    if canal:
        overwrite = discord.PermissionOverwrite(send_messages=True)
        await canal.set_permissions(guild.default_role, overwrite=overwrite)
        dono = guild.get_member(OWNER_ID)
        user = guild.get_member(USER_ID)
        if dono:
            await canal.set_permissions(dono, send_messages=True)
        if user:
            await canal.set_permissions(user, send_messages=True)
        logging.info("🔓 Canal desbloqueado para todos")
        return True
    return False

# =========================
# TAREFA DE CHECAGEM
# =========================
async def check_time_task():
    global canal_bloqueado, avisos_enviados
    agora = datetime.now()
    hora = agora.hour
    minuto = agora.minute

    guild = bot.get_guild(GUILD_ID)
    canal = guild.get_channel(CHANNEL_ID)

    # Avisos 30, 20 e 10 minutos antes do bloqueio
    if hora == 9 and minuto in [30, 40, 50]:
        if minuto not in avisos_enviados:
            if canal:
                mensagens = {
                    30: "⏰ Faltam **30 minutos** para o bloqueio do envio de mensagens! 🚫",
                    40: "⏰ Faltam **20 minutos** para o bloqueio do envio de mensagens! 🚫",
                    50: "⏰ Faltam **10 minutos** para o bloqueio do envio de mensagens! 🚫"
                }
                await canal.send(mensagens[minuto])
                avisos_enviados.add(minuto)
                logging.info(f"📢 Aviso enviado ({mensagens[minuto]})")

    # Bloqueio automatico
    if 10 <= hora < 19 and not canal_bloqueado:
        sucesso = await bloquear_canal()
        if sucesso:
            canal_bloqueado = True
            avisos_enviados.clear()
            if canal:
                await canal.send("🔒 O canal foi bloqueado para envio de mensagens.")
            logging.info(f"🔒 Canal bloqueado automaticamente as {agora.strftime('%H:%M')}")

    # Desbloqueio automatico
    elif (hora >= 19 or hora < 10) and canal_bloqueado:
        sucesso = await desbloquear_canal()
        if sucesso:
            canal_bloqueado = False
            if canal:
                await canal.send("🔓 O canal foi desbloqueado, todos podem falar agora! 🎉")
            logging.info(f"🔓 Canal desbloqueado automaticamente as {agora.strftime('%H:%M')}")

# =========================
# LOOP AUTOMATICO
# =========================
@tasks.loop(minutes=1)
async def check_time():
    await check_time_task()

# =========================
# EVENTOS
# =========================
@bot.event
async def on_ready():
    logging.info(f"✅ Bot logado como {bot.user}")
    check_time.start()
    # Checagem imediata ao iniciar
    await check_time_task()

# =========================
# COMANDOS MANUAIS
# =========================
@bot.command()
async def bloquear(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("🚫 Voce nao tem permissao para usar este comando.")
        return
    sucesso = await bloquear_canal()
    if sucesso:
        global canal_bloqueado
        canal_bloqueado = True
        await ctx.send("🔒 Canal bloqueado manualmente!")
    else:
        await ctx.send("⚠️ Nao consegui encontrar o canal.")

@bot.command()
async def desbloquear(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("🚫 Voce nao tem permissao para usar este comando.")
        return
    sucesso = await desbloquear_canal()
    if sucesso:
        global canal_bloqueado
        canal_bloqueado = False
        await ctx.send("🔓 Canal desbloqueado manualmente!")
    else:
        await ctx.send("⚠️ Nao consegui encontrar o canal.")

# =========================
# RODA O BOT
# =========================
bot.run(TOKEN)
