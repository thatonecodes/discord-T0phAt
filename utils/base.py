import discord
from discord.ext import commands
from utils import getIcon, getName
from discord.ui import Select, View
from typing import Dict, List, Optional, Callable 

# Initialize view classes
class DropdownView(View):
    """
    Utility class for initializing View Render class.
    ---
    Attributes:
        options `list[discord.SelectOption], optional`: List of discord.SelectOption for the dropdown menu.
        callback `Optional[Callable]`: Callback function to handle the interaction.
        timeout `Optional[float]`: Timeout for the view interaction in seconds. Defaults to 180.
    """
    def __init__(self, *, options: Optional[List[discord.SelectOption]]=None, callback: Optional[Callable]=None, timeout: Optional[float]= 180):
        super().__init__(timeout=timeout)
        self.add_item(DropdownMenu(options=options, callback=callback))

class DropdownMenu(Select):
    def __init__(self, *, options: Optional[List[discord.SelectOption]]=None, callback: Optional[Callable]=None):
        """
        Dropdown menu with custom callback support.
        ---
        Attributes:
            options `Optional[list[discord.SelectOption]]`: List of discord.SelectOption for the dropdown menu.
            callback `Optional[Callable]`: Callback function to handle the interaction.
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
        ---
        Attributes:
            interaction `discord.Interaction`: Discord interaction object.
        Raises:
            `Exception`: if the callback function is not provided.
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

    def add_fields(self, embed: discord.Embed, desiredList: List[Dict]) -> discord.Embed:
        """
        Adds fields to the embed, with optional inline setting.
        ---
        Attributes:
            embed `discord.Embed`: The embed to add fields to.
            desiredList `list[dict]`: List of fields, where each field is a dict with keys name, value, and optionally inline.

        Returns:
            `discord.Embed`: The updated embed.
        """
        for field in desiredList:
            name = field.get('name')
            value = field.get('value')
            inline = field.get('inline', False)  # Default is False if not specified
            embed.add_field(name=name, value=value, inline=inline)
        return embed

    async def send_embed(
            self, ctx: commands.Context | discord.Interaction, title: str, description: str, fields: Optional[List[Dict]] = None, 
            thumbnail: str = "", footer: Dict = {}, view=None, colour: discord.Colour = discord.Colour.random(), 
            ephemeral: bool = False, dropdown_options: Optional[List[discord.SelectOption]] = None, dropdown_callback: Optional[Callable] = None
        ) -> discord.Embed: 
        """
        Utility to send an embed with a consistent style.
        ---
        Attributes:
            ctx `commands.Context | discord.Interaction`: The command or interaction context.
            title `str`: The title of the embed.
            description `str`: The description of the embed.
            colour `discord.Colour, optional`: The color of the embed. Defaults to `discord.Colour.random()`.
            fields `list[dict], optional`: A list of fields, where each field is a dictionary with 
                name `str`, value `str`, and inline `bool`.
            thumbnail `str, optional`: A URL (https) for the embed thumbnail.
            footer `dict, optional`: A dictionary containing text `str` and icon `bool` or `str` for an image link.
            view `discord.ui.View, optional`: A reference to a `discord.ui.View` instance.
            ephemeral `bool, optional`: Whether the message should be ephemeral (for interactions).
            dropdown_options `list[discord.SelectOption], optional`: A list of `discord.SelectOption` items for a dropdown menu.
            dropdown_callback `Callable, optional`: An asynchronous function to handle dropdown selections.

        Returns:
            `discord.Embed`: The embed that was created and sent, if needed elsewhere.
        """
        # Fetch the icon details
        self.icon_file, self.icon_url = getIcon()

        # Prepare the embed
        embed = discord.Embed(
            title=title,
            description=description,
            colour=colour ,
        )
        embed.set_author(name=self.botname, icon_url=self.icon_url)
        if len(thumbnail) != 0:
            embed.set_thumbnail(url=thumbnail)
        if footer != {}:
            if isinstance(footer["icon"], bool):
                embed.set_footer(text=footer["text"], icon_url=self.icon_url if footer["icon"] else None)
            elif isinstance(footer["icon"], str):
                embed.set_footer(text=footer["text"], icon_url=footer["icon"] if footer["icon"] else None)
        if fields:
            embed = self.add_fields(embed, fields)

        # Initialize the dropdown view if options are provided
        view = view
        if dropdown_options:
            view = DropdownView(options=dropdown_options, callback=dropdown_callback) if dropdown_options else None

        # Function to send the embed
        async def send(embed, view, file=None):
            try: 
                if not file:
                    file = discord.File(fp="") #create empty discord file if none
                if isinstance(ctx, commands.Context):
                    await ctx.send(embed=embed, file=file, view=view)
                elif isinstance(ctx, discord.Interaction):
                    if not ctx.response.is_done():
                        await ctx.response.send_message(embed=embed, file=file, view=view, ephemeral=ephemeral)
                    else:
                        await ctx.followup.send(embed=embed, file=file, view=view, ephemeral=ephemeral)
            except Exception as e:
                pass
                # logger = get_logger()
                # logger.error("[ERR] While sending:", e)
                    
        # Send the embed
        await send(embed=embed, view=view, file=self.icon_file if self.icon_file else None)
        #return the embed object if needed elsewhere
        return embed

    @classmethod
    async def setup(cls, bot: commands.Bot, cog_class: type):
        """
        Class method to simplify the cog setup process.
        ---
        Attributes:
            bot `commands.Bot`: The bot instance.
            cog_class `type`: The cog class to instantiate and add to the bot.
        """
        # logger.debug("Setting up", bot, cog_class)

        await bot.add_cog(cog_class(bot))
