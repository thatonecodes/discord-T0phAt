from discord.ext import commands
from discord.ext.commands.errors import ExtensionAlreadyLoaded, NoEntryPointError
import discord
from dotenv import load_dotenv
import events 
import os
import asyncio
import traceback


load_dotenv()

#uneeded, but expriment
defaultguildID = os.getenv("DEFAULTGUILDID")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)


@bot.event                
async def loader():
    extensions = []
    for dirpath, dirnames, filenames in os.walk("./cogs"):
        for filename in filenames:
            if filename.endswith(".py"):
                cog_name = filename[:-3]  # Remove the ".py" extension
                if dirpath == "./cogs":
                    cog_path = f"cogs.{cog_name}"
                else:
                    rel_dir = os.path.relpath(dirpath, "./cogs")
                    cog_path = f"cogs.{rel_dir.replace('/', '.')}.{cog_name}"
                try:
                    await bot.load_extension(cog_path)
                    print(f"Loaded cog: {cog_path}")
                except ExtensionAlreadyLoaded:
                    pass
                except NoEntryPointError:
                    pass #passing due to base class function should be loading entry point
                except Exception as e:
                    print("ERROR")
                    traceback.print_exc()


@bot.event
async def on_ready():
    await events.on_ready(bot)

@bot.event
async def on_command_error(*args, **kwargs):
    await events.on_command_error(*args, **kwargs)

token = str(os.getenv("BOTTOKEN"))
if not token:
    raise Exception("No bot token was found! Did you create an .env file with BOTTOKEN var?")

async def main():
    async with bot:
        await loader()
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
