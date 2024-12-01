import discord
from discord.ext import commands
from discord import SelectOption, Interaction, Embed
from utils import BaseClass

class Helper(BaseClass):
   def __init__(self, bot) -> None:
        super().__init__(bot)

   def get_slash_commands(self):
       output_list = []
       #slashcommands, uses /slash prefix
       slash_commands = self.bot.tree.get_commands()
       for command in slash_commands:
           commands_description = "\n".join(
                [f"`/{command.name}` - {command.description or command.help or 'No description available'}"]
           )

           output_list.append({"name": command.name, "value": commands_description})
       return output_list

   def get_cog_commands(self):
       output_list = []
       #Cog commands - using the $cmd prefix...
       for cog_name, cog in self.bot.cogs.items():
           command_list = cog.get_commands()
           if command_list:
               commands_description = "\n".join(
                    [f"`{self.bot.command_prefix}{command.name}` - {command.help or 'No description available'}" for command in command_list]
               )

               output_list.append({"name": cog_name.lower(), "value": commands_description})
       return output_list


   async def dropdownCallback(self, interaction: Interaction, selectedValues):
       embed = Embed(
            title=f"Help ++ {selectedValues[0]}",
            description=f"Summary of all {selectedValues[0]}."
        )
       if "Cogs" in selectedValues:
           embed.set_footer(text=f"{self.bot.command_prefix}cmd")
           embed = self.add_fields(embed, self.get_cog_commands())
           embed.colour = discord.Color.blue()
       elif "Slash Commands" in selectedValues:
           embed.set_footer(text=f"/cmd")
           embed = self.add_fields(embed, self.get_slash_commands())
           embed.colour = discord.Color.green()
       await interaction.response.send_message(embed=embed)


   info = "Command that displays this message."
   @commands.command(help=info)
   async def help(self, ctx):
       fields = self.get_cog_commands() + self.get_slash_commands()

       await self.send_embed(
            ctx,
            title="Help ++ All commands",
            description="Summary of all commands!",
            fields=fields,
            dropdown_options=[
                SelectOption(label="Cogs", description=f"Regular prefixed commands with ({self.bot.command_prefix})", emoji="👾"),
                SelectOption(label="Slash Commands", description=f"Interaction commands with the slash /", emoji="🤝")
            ],
            dropdown_callback=self.dropdownCallback
        )
 

async def setup(bot):
    await BaseClass.setup(bot, Helper)
