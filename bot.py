import os
import discord
import random
import asyncio
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from strings import *


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

random_messages = [
    "AMİNAKEEEEE",
    "neco bumblebee olsam beni yine de sever miydin la",
    "durum ne ensar",
    "beyler kendimi turşu yaptım eheeeeeee",
    "memet sen misin la",
    "LETS PLAY FOOTBALL",
    "onları sağamazsın"
]

CHANNEL_ID = 1077904975902019676

async def send_random_messages():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    while not bot.is_closed():
        await asyncio.sleep(random.randint(1800, 3600))  # Random time between 30min to 1 Hour
        if channel is not None:
            message = random.choice(random_messages)
            await channel.send(message)

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} olarak giriş yaptı.")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

    bot.loop.create_task(send_random_messages())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() == "sa":
        await message.channel.send("as")
    await bot.process_commands(message)

@bot.command()
async def özet(ctx):
    await ctx.send("Ensar alianın eski manitle cp yapıyo sonra alihan ensarı banlıyo bizde tekrediyoz orayi")

@bot.command()
async def patlat(ctx):
    await ctx.send(trollface)
    
@bot.command()
async def amogus(ctx):
    await ctx.send(amongus)

@bot.command()
async def kaçcm(ctx):
    cm = random.randint(5,25)
    await ctx.send(cm, "\n", "8" + "=" * cm + "D")

@bot.command()
async def zar(ctx, num: int):
    if num > 1:
        roll = random.randint(1, num)
        await ctx.send(roll)
    else:
        await ctx.send(TypeError)

# Bans User
@bot.tree.command(name = "ban", description = "Ban User")
@app_commands.checks.has_permissions(ban_members = True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    try:
        await member.ban(reason = reason)
        await interaction.response.defer()
        await asyncio.sleep(4)
        sent_message = await interaction.followup.send_message(f"{member.name}] banlandı. Sebep: {reason}")
        await asyncio.sleep(5)
        await sent_message.delete()
    except Exception as e:
        await interaction.response.defer()
        await asyncio.sleep(4)
        error_message = await interaction.followup.send_message(f"Bir hata oluştu. {str(e)}")
        await asyncio.sleep(5)
        await error_message.delete() 

# If user doesn't have the permission to ban show error to only user.
@ban.error
async def ban_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        sent_message = await interaction.followup.send_message("Bu komutu kullanmak için gerekli olan izne sahip değilsiniz.", ephemeral = True)
        await asyncio.sleep(5)
        await sent_message.delete()

# Removes Messages
@bot.tree.command(name = "temizle", description = "Belirli sayıda mesajı sil")
@app_commands.checks.has_permissions(manage_messages = True)
async def temizle(interaction: discord.Interaction, amount: int):
    if amount > 0:
        deleted = await interaction.channel.purge(limit = amount)
        await interaction.response.defer()
        await asyncio.sleep(4)
        sent_message = await interaction.followup.send(f"{len(deleted)} mesaj başarıyla silindi.")
        await asyncio.sleep(5)
        await sent_message.delete()
    else:
        await interaction.response.defer()
        await asyncio.sleep(4)
        sent_message = await interaction.followup.send(f"Geçersiz sayı.")
        await asyncio.sleep(5)
        await sent_message.delete()

#If user doesn't have the permission to remove messages show error to only user.
@temizle.error
async def temizle_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        sent_message = await interaction.followup.send_message("Bu komutu kullanmak için gerekli olan izne sahip değilsiniz.", ephemeral = True)
        await asyncio.sleep(5)
        await sent_message.delete()

bot.run(TOKEN)
