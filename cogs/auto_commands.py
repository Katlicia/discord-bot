import discord
from discord.ext import commands, tasks
import pytz
from datetime import datetime, time
from others.helper_functions import check_keyword

class AutoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = 1077904974983479348
        self.last_birthday_check = None

    @tasks.loop(hours=2)
    async def birthday_message(self):
        today = datetime.now(pytz.timezone("Europe/Istanbul")).date()

        if self.last_birthday_check == today:
            return

        guild = self.bot.get_guild(self.guild_id)
        if not guild:
            return

        role = discord.utils.get(guild.roles, name="Dogum Gunu Cocugu")
        if not role:
            return

        members = [m for m in guild.members if role in m.roles]
        if not members:
            return

        channel = self.bot.get_channel(1077904975902019676)
        if not channel:
            return

        mentions = ", ".join(m.mention for m in members)
        await channel.send(f"🎉 Doğum günün kutlu olsun {mentions}")

        self.last_birthday_check = today

    @birthday_message.before_loop
    async def before_birthday_message(self):
        await self.bot.wait_until_ready()

    @tasks.loop(time=time(hour=8, tzinfo=pytz.timezone("Europe/Istanbul")))
    async def goodmorning_message(self):
        channel = self.bot.get_channel(1077904975902019676)
        if channel:
            await channel.send("gunaydin gencolar")

    async def cog_load(self):
        self.birthday_message.start()
        self.goodmorning_message.start()

    async def cog_unload(self):
        self.birthday_message.cancel()
        self.goodmorning_message.cancel()


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if check_keyword(message.content, "41"):
            await message.reply(":flag_tr:")
        if check_keyword(message.content, "17"):
            await message.reply(":flag_tr:")
        if message.content.lower() == "sa":
            await message.channel.send("as")
        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(AutoCommands(bot))
