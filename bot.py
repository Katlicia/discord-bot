import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from others.helper_functions import check_keyword

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Bot signed in as: {bot.user.name}")
    await bot.tree.sync()

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
