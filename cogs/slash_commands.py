import discord
from discord import app_commands
from discord.ext import commands

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bans User
    @app_commands.command(name="ban", description="Ban User")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"{member.name} is banned. Reason: {reason}", ephemeral=True, delete_after=5)
        except Exception as e:
            await interaction.response.send_message(f"An error happened: {str(e)}", ephemeral=True, delete_after=5)

    # Error handler for permission errors
    @ban.error
    async def ban_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True, delete_after=5)


    # Removes Messages
    @app_commands.command(name="temizle", description="Remove last X messages.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def temizle(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)
        if amount > 0:
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.followup.send(f"{len(deleted)} messages deleted successfully.", ephemeral=True)
        else:
            await interaction.followup.send("Invalid number.", ephemeral=True)

    # If user doesn't have the permission to remove messages show error to only user.
    @temizle.error
    async def temizle_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.followup.send("You can't use this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
