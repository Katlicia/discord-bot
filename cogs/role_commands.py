import discord
from discord.ext import commands
from discord.ui import Button, View, Select

class GenderAgeSelectView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    # Gender Buttons
    @discord.ui.button(label="Erkek", style=discord.ButtonStyle.primary, custom_id="gender_male")
    async def male_button(self, interaction: discord.Interaction, button: Button):
        await self.handle_gender_selection(interaction, "xx")
    
    @discord.ui.button(label="Kız", style=discord.ButtonStyle.primary, custom_id="gender_female")
    async def female_button(self, interaction: discord.Interaction, button: Button):
        await self.handle_gender_selection(interaction, "xy")

    # Age Select Menu
    @discord.ui.select(
        placeholder="Yaş Seçimi Yapın",
        options=[
            discord.SelectOption(label="18(-)", description="18 Yaş Altı", value="18(-)"),
            discord.SelectOption(label="18", description="18 Yaş", value="18"),
            discord.SelectOption(label="19", description="19 Yaş", value="19"),
            discord.SelectOption(label="20", description="20 Yaş", value="20"),
            discord.SelectOption(label="21", description="21 Yaş", value="21"),
            discord.SelectOption(label="22", description="22 Yaş", value="22"),
            discord.SelectOption(label="23(+)", description="23 Yaş Ve Üzeri", value="23(+)")
        ],
        custom_id="age_select"
    )
    async def age_select(self, interaction: discord.Interaction, select: Select):
        await self.handle_age_selection(interaction, select.values[0])

    # Gender Role
    async def handle_gender_selection(self, interaction: discord.Interaction, gender: str):
        guild = interaction.guild
        member = interaction.user
        roles_to_remove = ["xx", "xy"]  

        # Remove existing gender roles.
        for role_name in roles_to_remove:
            role = discord.utils.get(guild.roles, name=role_name)
            if role in member.roles:
                await member.remove_roles(role)

        # Add Gender role.
        new_role = discord.utils.get(guild.roles, name=gender)
        if new_role is None:
            # If role doesn't exist, create it.
            new_role = await guild.create_role(name=gender, reason=f"Otomatik olarak {gender} cinsiyeti için oluşturuldu.")
        
        await member.add_roles(new_role)
        await interaction.response.send_message(f"{gender} rolü size verildi.", ephemeral=True)

    # Age Role
    async def handle_age_selection(self, interaction: discord.Interaction, age_range: str):
        guild = interaction.guild
        member = interaction.user
        roles_to_remove = ["18(-)", "18", "19", "20", "21", "22", "23(+)"]

        # Remove existing age roles.
        for role_name in roles_to_remove:
            role = discord.utils.get(guild.roles, name=role_name)
            if role in member.roles:
                await member.remove_roles(role)

        # Add new age role.
        new_age_role = discord.utils.get(guild.roles, name=age_range)
        if new_age_role is None:
            # If role doesn't exist, create it.
            new_age_role = await guild.create_role(name=age_range, reason=f"Otomatik olarak {age_range} yaş aralığı için oluşturuldu.")
        
        await member.add_roles(new_age_role)
        await interaction.response.send_message(f"{age_range} rolü size verildi.", ephemeral=True)


# Send message and buttons.
class RoleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        roles_channel_id = 1281570111722881115
        roles_channel = self.bot.get_channel(roles_channel_id)
        
        # Search message
        found = False
        async for message in roles_channel.history(limit=100):
            # Check if message is sent.
            if message.author == self.bot.user and message.embeds:
                embed = message.embeds[0]
                if embed.title == "Rol Seçimi" and "Cinsiyet ve yaş rollerinizi aşağıdaki seçeneklerden seçebilirsiniz." in embed.description:
                    found = True
                    print("var")
                    break

        if not found:
            # Sent embed message if not found
            embed = discord.Embed(
                title="Rol Seçimi",
                description="Cinsiyet ve yaş rollerinizi aşağıdaki seçeneklerden seçebilirsiniz.",
                color=discord.Color.blurple()
            )
            embed.add_field(name="Cinsiyet Seçimi", value="Erkek veya Kız seçin.", inline=False)
            embed.add_field(name="Yaş Aralığı", value="15-18, 19, 20, 21, 22, 23+ yaş seçeneklerini seçin.", inline=False)
            embed.set_footer(text="Roller otomatik olarak atanacaktır.")
            
            view = GenderAgeSelectView(self.bot)
            await roles_channel.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(RoleCommands(bot))
