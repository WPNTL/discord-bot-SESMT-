import discord
from discord.ext import commands, tasks
from datetime import datetime
import logging

# =========================
# CONFIGURAÇÃO DE LOG
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),  # salva no arquivo bot.log
        logging.StreamHandler()           # continua mostrando no terminal
    ]
)

# =========================
# CONFIGURAÇÃO DO BOT
# =========================
TOKEN = "COLOQUE AQUI O TOKEN"

GUILD_ID = ID do servidor
CHANNEL_ID = ID do canal a ser controlado
OWNER_ID = ID do owner do server (autorizado a mandar mensagens quando bloqueado)
USER_ID = ID de outro user (autorizado a mandar mensagens)

canal_bloqueado = False

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# FUNÇÕES DE BLOQUEIO/DESBLOQUEIO
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
# EVENTOS
# =========================
@bot.event
async def on_ready():
    logging.info(f"✅ Bot logado como {bot.user}")
    check_time.start()  # start do loop automático

# =========================
# LOOP AUTOMÁTICO
# =========================
@tasks.loop(minutes=1)
async def check_time():
    global canal_bloqueado
    agora = datetime.now()
    hora = agora.hour

    if 10 <= hora < 19 and not canal_bloqueado:
        sucesso = await bloquear_canal()
        if sucesso:
            canal_bloqueado = True
            logging.info(f"🔒 Canal bloqueado automaticamente às {agora.strftime('%H:%M')}")

    elif (hora >= 19 or hora < 10) and canal_bloqueado:
        sucesso = await desbloquear_canal()
        if sucesso:
            canal_bloqueado = False
            logging.info(f"🔓 Canal desbloqueado automaticamente às {agora.strftime('%H:%M')}")

# =========================
# COMANDOS MANUAIS
# =========================
@bot.command()
async def bloquear(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("🚫 Você não tem permissão para usar este comando.")
        return
    sucesso = await bloquear_canal()
    if sucesso:
        global canal_bloqueado
        canal_bloqueado = True
        await ctx.send("🔒 Canal bloqueado manualmente!")
    else:
        await ctx.send("⚠️ Não consegui encontrar o canal.")

@bot.command()
async def desbloquear(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("🚫 Você não tem permissão para usar este comando.")
        return
    sucesso = await desbloquear_canal()
    if sucesso:
        global canal_bloqueado
        canal_bloqueado = False
        await ctx.send("🔓 Canal desbloqueado manualmente!")
    else:
        await ctx.send("⚠️ Não consegui encontrar o canal.")

# =========================
# RODA O BOT
# =========================
bot.run(TOKEN)
