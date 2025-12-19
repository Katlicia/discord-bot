import discord
from discord import app_commands
from discord.ext import commands
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import os

load_dotenv()

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = OpenAI(
            api_key=os.getenv("OPEN_AI_TOKEN")
        )

    async def ensure_log_channel(self, guild: discord.Guild):
        # Creates alo-log channel if doesn't exist. 
        log_channel = discord.utils.get(guild.text_channels, name="alo-log")
        if log_channel is None:
            # Handling channel permissions.
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),  # Default role can't see the channel.
                guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),  # Bot can see the channel and send messages.
            }

            # Checking roles.
            for role in guild.roles:
                if role.permissions.ban_members:
                    # Roles with ban permission can see the log. 
                    overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=False)
                else:
                    # Others can't.
                    overwrites[role] = discord.PermissionOverwrite(view_channel=False)

            # Creating channel.
            log_channel = await guild.create_text_channel("alo-log", overwrites=overwrites)
        return log_channel

    # Bans User
    @app_commands.command(name="ban", description="Ban User")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"{member.name} is banned. Reason: {reason}", ephemeral=True, delete_after=5)
            # Saves the process in alo-log.
            log_channel = await self.ensure_log_channel(interaction.guild)
            await log_channel.send(f"{interaction.user.name} banned {member.name}. Reason: {reason}")
        except Exception as e:
            await interaction.response.send_message(f"An error happened: {str(e)}", ephemeral=True, delete_after=5)

    # Error handler for permission errors.
    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("You don't have the permission to use this command.", ephemeral=True, delete_after=5)

    # Kicks User
    @app_commands.command(name="kick", description="Kick User")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"{member.name} is kicked. Reason: {reason}", ephemeral=True, delete_after=5)
            # Saves the process in alo-log.
            log_channel = await self.ensure_log_channel(interaction.guild)
            await log_channel.send(f"{interaction.user.name} kicked {member.name}. Reason: {reason}")
        except Exception as e:
            await interaction.response.send_message(f"An error happened: {str(e)}", ephemeral=True, delete_after=5)

    # Error handler for permission errors.
    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("You don't have the permission to use this command.", ephemeral=True, delete_after=5)

    # Removes Messages
    @app_commands.command(name="temizle", description="Remove last X messages.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def temizle(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)
        if amount > 0:
            deleted = await interaction.channel.purge(limit=amount)
            # Saves the process in alo-log
            log_channel = await self.ensure_log_channel(interaction.guild)
            await log_channel.send(f"{interaction.user.name} deleted {len(deleted)} messages in {interaction.channel.name}-channel.")
            await interaction.followup.send(f"{len(deleted)} messages deleted successfully.", ephemeral=True)
        else:
            await interaction.followup.send("Invalid number.", ephemeral=True)

    # If user doesn't have the permission to remove messages show error to only user.
    @temizle.error
    async def temizle_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.followup.send("You don't have the permission to use this command.", ephemeral=True)

    # OpenAI text bot
    @app_commands.command(name="chat", description="Alo botla konuş")
    @app_commands.checks.cooldown(1, 60, key=lambda i: i.user.id) # Limit 60 seconds per user
    async def chat(self, interaction: discord.Interaction, prompt: str):
        # Wait for response and send thinking state
        await interaction.response.defer(thinking=True, ephemeral=False)

        try:
            response = self.client.responses.create(
                model="gpt-5-mini",
                input=[
                    {
                        "role": "system",
                        "content": "You are a helpful Discord bot named Alo. Reply in Turkish unless the user asks otherwise. Keep answers concise."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_output_tokens=1000
            )

            answer = response.output_text
            
            if not answer or not answer.strip():
                answer = "Bir cevap üretilemedi..."

            # Discord has 2000 word limitation
            if len(answer) > 1900:
                answer = answer[:1900] + "..."
            await interaction.followup.send(answer)
        
        except OpenAIError as e:
            # Error caused by OpenAI
            error_message = "Şuan AI servisine ulaşılamıyor."
            
            error_text = str(e).lower()

            if "insufficient_quota" in error_text:
                error_message = "OpenAI Credits have run out. Contact the developer."
            elif "rate_limit" in error_text:
                error_message = "Rate limit exceeded. Try again later."
            elif "invalid_api_key" in error_text:
                error_message = "Key error. Contact the developer."
            elif "model_not_found" in error_text:
                error_message = "No model found."
            elif "permission" in error_text:
                error_message = "No access to this model."
            
            log_channel = await self.ensure_log_channel(interaction.guild)
            await log_channel.send(f"OpenAI error", error_message, str(e))

            await interaction.followup.send(error_message, ephemeral=True)
        
        except Exception as e:
            # Error caused by Discord
            await interaction.followup.send(
                f"Beklenmeyen bir hata oluştu {str(e)}", 
                ephemeral=True
                )
    
    @chat.error
    async def chat_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"Bu komutu tekrar kullanmak için **{int(error.retry_after)} saniye** beklemelisin.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Bir hata oluştu.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
