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

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if check_keyword(message.content, "31"):
        await message.channel.send("QWPEOIRTPOWEIORHOPOIKWRETPOLIHJKWRTLŞHGKWERFPOĞGWERF"),
    if check_keyword(message.content, "ibo"):
        await message.reply(":sob: :skull:")
    if check_keyword(message.content, "41"):
        await message.reply(":flag_tr:")
    if check_keyword(message.content, "17"):
        await message.reply(":flag_tr:")
    if message.content.lower() == "sa":
        await message.channel.send("as")
    await bot.process_commands(message)

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
