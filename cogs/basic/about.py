from utils import BaseClass, getName, getVersion
from discord.ext import commands
import discord
import psutil
import time
from events import uptime

class About(BaseClass):
    def __init__(self, bot) -> None:
        super().__init__(bot)
    
    info = "Shows bot information and author."

    @discord.app_commands.command(
        name="about", 
        description=info
    )
    async def about(self, ctx):
        aboutInfo = f"""{getName()} is the bot for all your needs.
        Need info? Need a web crawler? Need SSH? Server controls?
        Make your own commands suited to your needs.
        And make it your own with configuration to suite YOUR needs.

        Made with [discord.py](https://discordpy.readthedocs.io/en/stable/) v{discord.__version__} 
        """

        memory = psutil.virtual_memory()

        # Memory usage percentage
        mem_percent = memory.percent
        
        memoryUsageValue = f"{mem_percent}%"

        fields = [
            {"name": "Current Botname 📖", "value": getName(), "inline": True},
            {"name": "CPU Usage 🖥️", "value": f"{psutil.cpu_percent(interval=1)}%","inline": True},
            {"name": "Memory Usage 💾", "value": f"{memoryUsageValue}","inline": True},
            {"name": "Latency 😅", "value": f"{round(self.bot.latency * 1000)}ms","inline": True}, # Convert from seconds to milliseconds
            {"name": "Server Count 😐", "value": f"{len(self.bot.guilds)}","inline": True},
            {"name": "Version 📊", "value": getVersion(),"inline": True},
            {"name": "Status 🔧", "value": f"{self.bot.status}","inline": True},
            {"name": "Activity ⚙️", "value": f"{self.bot.activity}","inline": True},
            {"name": "Uptime 👍", "value": f"{(time.time() - uptime) / 60:.2f} minutes", "inline": True},
        ]

        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/PqmxFp8NBp", style=discord.ButtonStyle.link))
        await self.send_embed(
            ctx,
            title=f"About {getName()}",
            description=aboutInfo,
            fields=fields,
            footer={"text": "Made by Michael", "icon": "https://cdn.discordapp.com/avatars/1278929631197663314/fab7b0f06b4b5fadd061189a56a1711e.webp?size=160"},
            view=view,
            colour=discord.Colour.from_rgb(252, 5, 33)
        )

async def setup(bot):
    await BaseClass.setup(bot, About)
