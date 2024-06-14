import os
import discord
import random
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from dotenv import load_dotenv
from discord import app_commands
import pytz
import re
from strings import *

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True  # Üye verilerine erişmek için gerekli
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

random_messages = [
    "AMİNAKEEEEE",
    "neco bumblebee olsam beni yine de sever miydin la",
    "durum ne ensar",
    "beyler kendimi turşu yaptım eheeeeeee",
    "memet sen misin la",
    "LETS PLAY FOOTBALL",
    "onları sağamazsın",
    "kufredecem"
]

CHANNEL_ID = 1077904975902019676

async def send_random_messages():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    while not bot.is_closed():
        await asyncio.sleep(random.randint(18000, 43200))  # 5H-12H
        if channel is not None:
            message = random.choice(random_messages)
            await channel.send(message)

@tasks.loop(hours=10)
async def birthday_message():
    channel = bot.get_channel(1077904975902019676)
    guild = bot.get_guild(1077904974983479348)
    role = discord.utils.get(guild.roles, name="Dogum Gunu Cocugu")
    if role is None:
        print(f"Rol bulunamadı.")
        return
    members_with_role = [member for member in guild.members if role in member.roles]
    if members_with_role:
        member_mentions = ", ".join([member.mention for member in members_with_role])
        await channel.send(f"Doğum günün kutlu olsun {member_mentions}")

@birthday_message.before_loop
async def before_birthday_message():
    await bot.wait_until_ready()

# 31 Text Control
def is_pure_text(content):
    url_pattern = r'(https?://\S+|www\.\S+)'  # URL
    mention_pattern = r'(<@!?&?\d+>)'  # Mentions
    emoji_pattern = r'(<a?:\w+:\d+>)'  # Custom emotes

    content = re.sub(url_pattern, '', content)
    content = re.sub(mention_pattern, '', content)
    content = re.sub(emoji_pattern, '', content)

    return "31" in content

async def send_goodmorning_message():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    turkey_tz = pytz.timezone('Europe/Istanbul')
    while not bot.is_closed():
        now = datetime.now(turkey_tz)
        target_time = now.replace(hour=10, minute=0, second=0, microsecond=0)
        if now > target_time:
            target_time += timedelta(days=1)
        wait_time = (target_time - now).total_seconds()
        await asyncio.sleep(wait_time)
        if channel is not None:
            await channel.send("gunaydin gencolar")

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} olarak giriş yaptı.")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

    bot.loop.create_task(send_random_messages())
    bot.loop.create_task(send_goodmorning_message())
    bot.loop.create_task(daily_mention())
    birthday_message.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if is_pure_text(message.content):
        await message.channel.send("QWPEOIRTPOWEIORHOPOIKWRETPOLIHJKWRTLŞHGKWERFPOĞGWERF")
    if message.content.lower() == "sa":
        await message.channel.send("as")
    if message.author.id == 316608072669986816:  # author ID
        if message.content.lower() == "kufredecem":
            await message.channel.send("amcik")
    await bot.process_commands(message)

async def daily_mention():
    await bot.wait_until_ready()
    channel = bot.get_channel(1077907619630546994)
    user = await bot.fetch_user(673274021567004712)
    
    while not bot.is_closed():
        now = datetime.now()
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        random_time = now.replace(hour=random_hour, minute=random_minute, second=0, microsecond=0)

        if random_time < now:
            random_time += timedelta(days=1)

        wait_time = (random_time - now).total_seconds()
        await asyncio.sleep(wait_time)
        
        await channel.send(f'{user.mention} merasim')
        await asyncio.sleep(24 * 60 * 60)


### "!" Commands

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
async def duyuru(ctx):
    await ctx.send("ibo olayi (gerisini biliyorsunuz)")

@bot.command()
async def kaçcm(ctx):
    
    cm = random.randint(5, 25)
    await ctx.send(f"{cm} cm \n{'8' + '=' * cm + 'D'}")

@bot.command()
async def zar(ctx, num: int):
    if num >= 1:
        roll = random.randint(1, num)
        await ctx.send(roll)
    else:
        await ctx.send("Geçersiz sayı!")

@bot.command()
async def birlestir(ctx, *args):
    if not args:
        await ctx.send("En az bir kelime ekle")
        return
    def get_random_letter(word):
        word_len = len(word)
        if word_len <= 3:
            return word
        choice = random.choice(["start", "middle", "end"])
        if choice == "start":
            return word[:3]
        elif choice == "middle":
            start = word_len // 2 - 1
            return word[start:start + 3]
        elif choice == "end":
            return word[-3:]
    
    letters = []
    for word in args:
        letters.append(get_random_letter(word))
    combined_word = "".join(letters)
    await ctx.send(combined_word)

#### "/" Commands

# Bans User
@bot.tree.command(name="ban", description="Ban User")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member.name} banlandı. Sebep: {reason}", ephemeral=True, delete_after=5)
    except Exception as e:
        await interaction.response.send_message(f"Bir hata oluştu: {str(e)}", ephemeral=True, delete_after=5)

# If user doesn't have the permission to ban show error to only user.
@ban.error
async def ban_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("Bu komutu kullanmak için gerekli olan izne sahip değilsiniz.", ephemeral=True, delete_after=5)

# Removes Messages
@bot.tree.command(name="temizle", description="Belirli sayıda mesajı sil")
@app_commands.checks.has_permissions(manage_messages=True)
async def temizle(interaction: discord.Interaction, amount: int):
    if amount > 0:
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"{len(deleted)} mesaj başarıyla silindi.", ephemeral=True, delete_after=5)
    else:
        await interaction.response.send_message("Geçersiz sayı.", ephemeral=True, delete_after=5)

# If user doesn't have the permission to remove messages show error to only user.
@temizle.error
async def temizle_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("Bu komutu kullanmak için gerekli olan izne sahip değilsiniz.", ephemeral=True, delete_after=5)

bot.run(TOKEN)
