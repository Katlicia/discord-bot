import discord
from discord.ext import commands
from others.variables import *
import random
import json
import requests
from config import *

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sent_hug_gifs = set()
        self.sent_kiss_gifs = set()
        self.sent_slap_gifs = set()
        self.TENOR_TOKEN = TENOR_TOKEN

    ### "!" Commands

    @commands.command(aliases = ["özet", "olay"])
    async def ozet(self, ctx):
        await ctx.send("Ensar alianın eski manitle cp yapıyo sonra alihan ensarı banlıyo bizde tekrediyoz orayi")

    @commands.command()
    async def patlat(self, ctx):
        await ctx.send(trollface)

    @commands.command()
    async def duyuru(self, ctx):
        await ctx.send("ibo olayi (gerisini biliyorsunuz)") 


    @commands.command()
    async def zar(self, ctx, num: int):
        if num >= 1:
            roll = random.randint(1, num)
            await ctx.send(roll)
        else:
            await ctx.send("Invalid number!")


    @commands.command()
    async def boy(self, ctx, height: int):
        if height <= 100:
            await ctx.send("?")
        elif height >= 300:
            await ctx.send("?")
        else:
            await ctx.send(f"Boyunuz {height} cm.")


    # Sends general avatar of member.
    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        if member.avatar != member.default_avatar:
            avatar_url = member.avatar.url
        else:
            avatar_url = member.default_avatar
        await ctx.send(f"{avatar_url}")


    # Sends server avatar of member.
    @commands.command()
    async def savatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        if member.avatar != member.default_avatar:
            avatar_url = member.guild_avatar.url
        else:
            avatar_url = member.default_avatar
        await ctx.send(f"{avatar_url}")


    # Sends avatar of server.
    @commands.command()
    async def avatarsv(self, ctx):
        server = ctx.guild
        if server.icon:
            icon_url = server.icon.url
            await ctx.send(icon_url)
        else:
            await ctx.send("Image not found.")


    # Sends banner of server.
    @commands.command()
    async def bannersv(self, ctx):
        server = ctx.guild
        if server.banner:
            banner_url = server.banner.url
            await ctx.send(banner_url)
        else:
            await ctx.send("Banner not found.")


    # Sends banner of member.
    @commands.command()
    async def banner(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        user = await self.bot.fetch_user(member.id)
        banner_url = user.banner.url if user.banner else "Banner not found."
        await ctx.send(f"{banner_url}")


    # Finds city name by plate vice versa. (Turkiye only.)
    @commands.command()
    async def plaka(self, ctx, city: str):
        found = False
        if city.isdigit():
            plate_num = int(city)
            for plate, name in cities:
                if plate_num == int(plate):
                    await ctx.send(f"{plate_num} numaralı plaka {name} ilinindir.")
                    found = True
                    break
            if not found:
                await ctx.send("Geçersiz plaka.")
        else:
            city_lower = city.lower()
            for plate, name in cities:
                if city_lower == name.lower():
                    await ctx.send(f"{name.capitalize()} şehrinin plakası {plate}'dır.")
                    found = True
                    break
            if not found:
                await ctx.send("Geçersiz şehir.")

    # Creates new words based of given words.
    @commands.command()
    async def birlestir(self, ctx, *args):
        if not args:
            await ctx.send("Add at least one word.")
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


    # Sent gifs are stored in sent_gifs set so same gif is not sent twice.
    # Sends an anime themed slap gif.
    @commands.command()
    async def slap(self, ctx, member: discord.Member):
        ckey = "my_test_app"
        lmt = 50
        search_term = "anime slap"  
        url = f"https://tenor.googleapis.com/v2/search?q={search_term}&key={self.TENOR_TOKEN}&client_key={ckey}&limit={lmt}"
        
        # If set length is greater than limit clear the set.
        if len(self.sent_slap_gifs) >= 50:
            self.sent_slap_gifs.clear()

        response = requests.get(url)
        if response.status_code == 200:
            top_gifs = json.loads(response.content)
            
            gifs = top_gifs.get('results', [])
            
            # Save GIF's.
            gif_urls = []
            gif_ids = []
            for gif in gifs:
                gif_id = gif.get('id')
                media_formats = gif.get('media_formats', {})
                gif_url = media_formats.get('gif', {}).get('url')
                if gif_url and gif_id not in self.sent_slap_gifs:
                    gif_urls.append(gif_url)
                    gif_ids.append(gif_id)
            
            if gif_urls:
                # If GIF is sent generate new GIF.
                chosen_index = random.randint(0, len(gif_urls) - 1)
                chosen_gif = gif_urls[chosen_index]
                chosen_gif_id = gif_ids[chosen_index]
                
                # Save sent GIF's.
                self.sent_slap_gifs.add(chosen_gif_id)
                embed = discord.Embed(description=f"")
                embed.set_image(url=chosen_gif)
                embed.set_author(name=f"{ctx.author.display_name} slaps {member.display_name}!", icon_url=ctx.author.avatar.url)
                embed.color = discord.Color.blue()  # This adds the blue line to the embed
                await ctx.send(embed=embed)
            else:
                await ctx.send("No GIF available.")
        else:
            await ctx.send("Can't access to API.")


    # Sent gifs are stored in sent_gifs set so same gif is not sent twice.
    # Sends an anime themed kiss gif.
    @commands.command()
    async def kiss(self, ctx, member: discord.Member):
        ckey = "my_test_app"
        lmt = 50
        search_term = "anime kiss"  
        url = f"https://tenor.googleapis.com/v2/search?q={search_term}&key={self.TENOR_TOKEN}&client_key={ckey}&limit={lmt}"
        
        # If set length is greater than limit clear the set.
        if len(self.sent_kiss_gifs) >= 50:
            self.sent_kiss_gifs.clear()

        response = requests.get(url)
        if response.status_code == 200:
            top_gifs = json.loads(response.content)
            
            gifs = top_gifs.get('results', [])
            
            # Save GIF's.
            gif_urls = []
            gif_ids = []
            for gif in gifs:
                gif_id = gif.get('id')
                media_formats = gif.get('media_formats', {})
                gif_url = media_formats.get('gif', {}).get('url')
                if gif_url and gif_id not in self.sent_kiss_gifs:
                    gif_urls.append(gif_url)
                    gif_ids.append(gif_id)
            
            if gif_urls:
                # If GIF is sent generate new GIF.
                chosen_index = random.randint(0, len(gif_urls) - 1)
                chosen_gif = gif_urls[chosen_index]
                chosen_gif_id = gif_ids[chosen_index]
                
                # Save sent GIF's.
                self.sent_kiss_gifs.add(chosen_gif_id)
                
                embed = discord.Embed(description=f"")
                embed.set_image(url=chosen_gif)
                embed.set_author(name=f"{ctx.author.display_name} kisses {member.display_name}!", icon_url=ctx.author.avatar.url)
                embed.color = discord.Color.blue()  # This adds the blue line to the embed
                await ctx.send(embed=embed)
            else:
                await ctx.send("No GIF available.")
        else:
            await ctx.send("Can't access the API.")


    # Sent gifs are stored in sent_gifs set so same gif is not sent twice.
    # Sends an anime themed hug gif.
    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        ckey = "my_test_app"
        lmt = 50
        search_term = "anime hug"  
        url = f"https://tenor.googleapis.com/v2/search?q={search_term}&key={self.TENOR_TOKEN}&client_key={ckey}&limit={lmt}"
        
        # If set length is greater than limit clear the set.
        if len(self.sent_hug_gifs) >= 50:
            self.sent_hug_gifs.clear()

        response = requests.get(url)
        if response.status_code == 200:
            top_gifs = json.loads(response.content)
            
            gifs = top_gifs.get('results', [])
            
            # Save GIF's.
            gif_urls = []
            gif_ids = []
            for gif in gifs:
                gif_id = gif.get('id')
                media_formats = gif.get('media_formats', {})
                gif_url = media_formats.get('gif', {}).get('url')
                if gif_url and gif_id not in self.sent_hug_gifs:
                    gif_urls.append(gif_url)
                    gif_ids.append(gif_id)
            
            if gif_urls:
                # If GIF is sent generate new GIF.
                chosen_index = random.randint(0, len(gif_urls) - 1)
                chosen_gif = gif_urls[chosen_index]
                chosen_gif_id = gif_ids[chosen_index]
                
                # Save sent GIF's.
                self.sent_hug_gifs.add(chosen_gif_id)

                embed = discord.Embed(description=f"")
                embed.set_image(url=chosen_gif)
                embed.set_author(name=f"{ctx.author.display_name} hugs {member.display_name}!", icon_url=ctx.author.avatar.url)
                embed.color = discord.Color.blue()  # This adds the blue line to the embed
                await ctx.send(embed=embed)
            else:
                await ctx.send("No GIF available.")
        else:
            await ctx.send("Can't access to API.")


    # Sends "No" gif.
    @commands.command()
    async def zaza(self, ctx):
        await ctx.send("https://media.discordapp.net/attachments/1077907619630546994/1270005477387796530/angry.gif?ex=66b22045&is=66b0cec5&hm=0be0ee514b1661a6a2cb922cdee63009ee88eb667c673fe8cffad1d16f81615b&=")


    # Sends active command list.
    @commands.command()
    async def commands(self, ctx):
        await ctx.send(
        """\
    >>> # ! Commands
    - *`avatar`* - Retrieves desired users general profile picture.
    - *`savatar`* - Retrieves desired users server profile picture.
    - *`avatarsv`* - Retrieves server icon.
    - *`banner`* - Retrieves desired users banner picture.
    - *`bannersv`* - Retrieves server banner.
    - *`patlat`* - Sends an ASCII image of trollface.
    - *`zar`* - Sends an integer between 1-(Desired Number).
    - *`birlestir`* - Sends a random word combined from given words.
    - *`slap`* - Sends an anime themed slap gif.
    - *`kiss`* - Sends an anime themed kiss gif.
    - *`hug`* - Sends an anime themed hug gif.
    - *`plaka`* - Returns desired city's plate number vice versa.
    - *`boy`* - Returns given height.
    - *`zaza`* - Returns an angry "no" gif. \n
    # / Commands
    - *`ban`* (Admin) - Bans user.
    - *`kick`* (Admin) - Kicks user.
    - *`temizle`* (Admin) - Clears last X messages from chat."""
    )   

async def setup(bot):
    await bot.add_cog(Commands(bot))
