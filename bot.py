import os
import discord
import random
import asyncio
from discord.ext import commands
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
    bot.loop.create_task(send_random_messages())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "sa" or "Sa" or "SA" or "sA":
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
    await ctx.send(amogus)

bot.run(TOKEN)
