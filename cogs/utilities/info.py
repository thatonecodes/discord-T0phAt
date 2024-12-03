from utils import BaseClass
import discord
from discord.ext import commands

class ExtractInfo(BaseClass):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    @commands.command(name="guserinfo", help="Global information about any user - use is `$guserinfo (userID)`")
    async def guserinfo(self, ctx, user_id: int):
        # Fetch user object using their ID
        try:
            user_id = int(user_id)
            user = await self.bot.fetch_user(user_id)
        except discord.NotFound:
            await self.send_embed(ctx, title="User not found!", description="HTTP request returned 404 Not Found!", colour=discord.Color.red())
            return
        except discord.HTTPException:
            await self.send_embed(ctx, title="Failed to fetch user information", description="Whoops! We couldn't process that.", colour=discord.Color.red())
            return
    
        
        # Prepare embed with user details
        fields = [
            {"name":"Username", "value":f"{user.name}#{user.discriminator}", "inline":True},
            {"name":"User ID", "value": user.id, "inline":True},
            {"name":"Bot Account", "value": user.bot, "inline":True},
            {"name": "Account Created", "value": user.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"), "inline": True}        
        ]
        await self.send_embed(
            ctx,
            title=f"User Information for {user.name}",
            description="Uses global discord snowflake API to gather data.",
            colour=discord.Color.blurple(),
            fields=fields,
            thumbnail=user.avatar.url
        )

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

        fields = [
            {"name": "Username", "value": user.name, "inline": True},
            {"name":"Discriminator", "value":f"#{user.discriminator}", "inline":True},
            {"name":"ID", "value":user.id, "inline":True},
            {"name":"Bot", "value":"Yes" if user.bot else "No", "inline":True},
            {"name":"Created At", "value": user.created_at.strftime("%Y-%m-%d %H:%M:%S"), "inline":True},
        ]
        if interaction.guild:
            member = interaction.guild.get_member(user.id)
            if member:
                fields.append({"name": "Nickname", "value": member.nick if member.nick else "No Nickname", "inline": True})
                if member.joined_at:
                    fields.append({"name": "Joined Server", "value": member.joined_at.strftime("%Y-%m-%d %H:%M:%S UTC"), "inline": True})
                roles = [role.name for role in member.roles]
                fields.append({"name": "Roles", "value": ", ".join(roles), "inline": False})

        await self.send_embed(
            interaction,
            title=f"Information for {user.name}",
            description=f"Details about {user.mention}",
            colour=discord.Colour.orange(),
            fields=fields,
            thumbnail=user.avatar.url if user.avatar else ""
        )

# Setup the cog
async def setup(bot):
    await BaseClass.setup(bot, ExtractInfo)
