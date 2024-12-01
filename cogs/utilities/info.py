from utils import BaseClass
import discord

class ExtractInfo(BaseClass):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    info = "Gets information like username and ID of user."
    @discord.app_commands.command(
        name="getinfo",
        description="Get information about a user."
    )
    async def getinfo(self, interaction: discord.Interaction, user: discord.User):
        """
        Command to get information about a user.
        :param interaction: The interaction object
        :param user: The user to fetch information about
        """
        embed = discord.Embed(
            title=f"Information for {user.name}",
            description=f"Details about {user.mention}",
            colour=discord.Colour.orange(),
        )
        embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
        embed.add_field(name="Username", value=user.name, inline=True)
        embed.add_field(name="Discriminator", value=f"#{user.discriminator}", inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Bot", value="Yes" if user.bot else "No", inline=True)
        embed.add_field(name="Created At", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)

        await interaction.response.send_message(embed=embed)

# Setup the cog
async def setup(bot):
    await BaseClass.setup(bot, ExtractInfo)
