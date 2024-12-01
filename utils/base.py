import discord
from discord.ext import commands
from utils import getIcon, getName
from discord.ui import Select, View
from typing import Dict, List, Optional


# Initialize view classes
class DropdownView(View):
    """
    Utility class for initializing View Render class.
    """
    def __init__(self, *, options=None, callback=None, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.add_item(DropdownMenu(options=options, callback=callback))

class DropdownMenu(Select):
    def __init__(self, *, options=None, callback=None):
        """
        Dropdown menu with custom callback support.
        :param options: List of discord.SelectOption for the dropdown menu.
        :param callback: Callback function to handle the interaction.
        """
        self.customCallback = callback
        if options is None:
            options = [
                discord.SelectOption(label="Option 1", description="This is the first option", emoji="1️⃣"),
                discord.SelectOption(label="Option 2", description="This is the second option", emoji="2️⃣"),
                discord.SelectOption(label="Option 3", description="This is the third option", emoji="3️⃣"),
            ]
        super().__init__(placeholder="Make a selection", options=options)

    async def callback(self, interaction: discord.Interaction):
        """
        Handles the selection callback and passes the interaction to the custom callback.
        :param interaction: Discord interaction object.
        """
        if callable(self.customCallback):
            await self.customCallback(interaction, self.values)
        else:
            raise Exception("[ERROR] callback function not provided, or is uncallable! It must be async.")

class BaseClass(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.embed = discord.Embed()
        self.botname = getName()
        self.icon_file, self.icon_url = getIcon()

    def add_fields(self, embed: discord.Embed, desiredList: List[Dict]):
        """
        Adds fields to the embed, with optional inline setting.
        :param embed: The embed to add fields to
        :param desiredList: List of fields, where each field is a dict with keys `name`, `value`, and optionally `inline`
        :return: The updated embed
        """
        for field in desiredList:
            name = field.get('name')
            value = field.get('value')
            inline = field.get('inline', False)  # Default is False if not specified
            embed.add_field(name=name, value=value, inline=inline)
        return embed

    async def send_embed(
            self, ctx, title, description, fields=None, footer: Dict = {}, colour=None, ephemeral=False, dropdown_options=None, dropdown_callback=None
        ):
        """
        Utility to send an embed with a consistent style.
        :param ctx: Command context or interaction context
        :param title: Title of the embed
        :param description: Description of the embed
        :param colour: Color of Discord Embed (default=discord.Colour.random())
        :param fields: (optional) List of fields, each a dict with `name`, `value`, `inline`
        :param footer: (optional) Dict {text: str, icon: bool}
        :param ephemeral: (optional) Whether the message should be ephemeral (for interactions)
        :param dropdown_options: (optional) List of `discord.SelectOption` for the dropdown menu
        :param dropdown_callback: (optional) Callback for the dropdown menu (has to be async func)
        """
        # Fetch the icon details
        self.icon_file, self.icon_url = getIcon()

        # Prepare the embed
        embed = discord.Embed(
            title=title,
            description=description,
            colour=colour or discord.Colour.random(),
        )
        embed.set_author(name=self.botname, icon_url=self.icon_url)
        if footer != {}:
            embed.set_footer(text=footer["text"], icon_url=self.icon_url if footer["icon"] else None)
        if fields:
            embed = self.add_fields(embed, fields)

        # Initialize the dropdown view if options are provided
        view = DropdownView(options=dropdown_options, callback=dropdown_callback) if dropdown_options else None

        # Function to send the embed
        async def send(embed, view, file=None):
            if not file:
                file = discord.File(fp="") #create empty discord file if none
            if isinstance(ctx, commands.Context):
                await ctx.send(embed=embed, file=file, view=view)
            elif isinstance(ctx, discord.Interaction):
                if not ctx.response.is_done():
                    await ctx.response.send_message(embed=embed, file=file, view=view, ephemeral=ephemeral)
                else:
                    await ctx.followup.send(embed=embed, file=file, view=view, ephemeral=ephemeral)

        # Send the embed
        await send(embed=embed, view=view, file=self.icon_file if self.icon_file else None)

    @classmethod
    async def setup(cls, bot, cog_class):
        """
        Class method to simplify the cog setup process.
        :param bot: The bot instance
        :param cog_class: The cog class to instantiate and add to the bot
        """
        print("Setting up", bot, cog_class)
        await bot.add_cog(cog_class(bot))
