import discord
from discord.ext import commands, tasks
import asyncio
import pytz
from datetime import datetime, timedelta
from others.helper_functions import check_keyword

class AutoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
        self.channel = None
        self.guild = bot.get_guild(1077904974983479348)
        self.birthday_message.start()
        self.bot.loop.create_task(self.send_goodmorning_message())

    @tasks.loop(hours=15)
    async def birthday_message(self):
        role = discord.utils.get(self.guild.roles, name="Dogum Gunu Cocugu")
        if role is None:
            print("Role not found.")
            return
        members_with_role = [member for member in self.guild.members if role in member.roles]
        if members_with_role:
            member_mentions = ", ".join([member.mention for member in members_with_role])
            if self.channel is None:
                self.channel = self.bot.get_channel(1077904975902019676)
            await self.channel.send(f"Doğum günün kutlu olsun {member_mentions}")

    @birthday_message.before_loop
    async def before_birthday_message(self):
        await self.bot.wait_until_ready()

    async def send_goodmorning_message(self):
        await self.bot.wait_until_ready()

        if self.channel is None:
            self.channel = self.bot.get_channel(1077904975902019676)
        
        turkey_tz = pytz.timezone('Europe/Istanbul')

        while not self.bot.is_closed():
            now = datetime.now(turkey_tz)
            target_time = now.replace(hour=10, minute=00, second=0, microsecond=0)
            
            if now > target_time:
                target_time += timedelta(days=1)

            wait_time = (target_time - now).total_seconds()
            await asyncio.sleep(wait_time)

            if self.channel is not None:
                await self.channel.send("gunaydin gencolar")

    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if check_keyword(message.content, "31"):
            await message.channel.send("QWPEOIRTPOWEIORHOPOIKWRETPOLIHJKWRTLŞHGKWERFPOĞGWERF")
        if check_keyword(message.content, "ibo"):
            await message.reply(":sob: :skull:")
        if check_keyword(message.content, "41"):
            await message.reply(":flag_tr:")
        if check_keyword(message.content, "17"):
            await message.reply(":flag_tr:")
        if message.content.lower() == "sa":
            await message.channel.send("as")
        if message.author.id == 316608072669986816:  # author ID
            if message.content.lower() == "kufredecem":
                await message.channel.send("amcik")
        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(AutoCommands(bot))
