from utils import BaseClass
import discord
from discord.ext import commands

class MessageControl(BaseClass):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    info = f"Sends a message to the specified user."
    @discord.app_commands.command(
        name="sendmsg",
        description=info
    )
    async def sendmsg(self, interaction: discord.Interaction, user: discord.User, message: str):
        """
        Command to send a message from the bot to another user.
        :param interaction: The interaction object
        :param user: The user to fetch information about
        :param message: The message you want to send using the bot (must be str) 
        """
        try:
            await user.send(message)
            await interaction.response.send_message(f"Message sent to {user.mention}.", ephemeral=True)
        except discord.Forbidden:
            await self.send_embed(
                interaction,
                title="ERROR: 401 Forbidden",
                description=f"Unable to send a message to {user.mention}. They might have DMs disabled.",
                colour=discord.Color.red(),
                ephemeral=True
            )

    @commands.command(help="Sends a message to provided user. Use - `$sendmsgid (userId)`")
    async def sendmsgid(self, ctx, user_id: int, *, message: str):
        """Sends a DM to a user by their ID."""
        try:
            user = await self.bot.fetch_user(user_id)  # Fetch the user by ID
            await user.send(message)  # Send a direct message
            await ctx.send(f"Message sent to {user.name}!")
        except discord.Forbidden:
            await ctx.send("I cannot send a DM to this user. They may have DMs disabled.")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to send the message: {e}")

    @commands.command(help="Repeats the message you provide it as an argument. usage: `$repeat (message)`")
    async def repeat(self, ctx, message: str):
        """
        Command to repeat a user message.
        """
        try:
            await ctx.send(message)
        except discord.Forbidden:
            await self.send_embed(
                ctx,
                title="ERROR: 401 Forbidden",
                description=f"Unable to send a message in this channel!",
                colour=discord.Color.red(),
                ephemeral=True
            )


async def setup(bot):
    await BaseClass.setup(bot, MessageControl)
