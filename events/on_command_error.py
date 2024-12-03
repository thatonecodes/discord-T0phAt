import discord
import logging, traceback
from discord.ext import commands
from discord.file import File
from utils import getIcon, getName
# from pathlib import Path

# env_path = Path(__file__).resolve().parent.parent / ".env"

botname: str = getName()

async def generic_error(ctx: commands.Context, icon_file: File | None, icon_url: str, error):
    errorembed = discord.Embed(
        title="An error occured!",
        description=f"Woah! Looks like there was an error!\n\n{str(error)}",
        color=discord.Colour.red()
    )
    errorembed.set_author(
        name=f"{botname}",
        icon_url=f"{icon_url}" 
    )
    if icon_file:
        await ctx.send(embed=errorembed, file=icon_file)
    else:
        logging.warn("[WARN] There was an issue with the icon file, using NO icon file.")
        await ctx.send(embed=errorembed)


def print_err(error):
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR)
    logging.error("[ERR] An error occurred during the execution of the script! Running traceback...")
    traceback.print_exception(type(error), error, error.__traceback__)

async def on_command_error(ctx, error):
    icon_file, icon_url = getIcon()
    if isinstance(error, commands.CommandNotFound):
        notfound = discord.Embed(
            title="Command not found!",
            description="Invalid command. Use /help to see all available commands.",
            color=discord.Color.red()
        )
        notfound.set_author(
            name=f"{botname}",
            icon_url=f"{icon_url}" 
        )
        await ctx.send(embed=notfound, file=icon_file)
    elif isinstance(error, commands.MissingPermissions):
        notfound = discord.Embed(
            title="Missing Permissions! :angry:",
            description="You do not have the permissions to run this command.",
            color=discord.Color.red()
        )
        notfound.set_author(
            name=f"{botname}",
            icon_url=f"{icon_url}"
        )
        await ctx.send(embed=notfound, file=icon_file)
    elif isinstance(error, commands.MissingRequiredArgument):
        notfound = discord.Embed(
            title="Missing argument! :neutral_face:",
            description="You did not include a required argument. Please try again!",
            color=discord.Color.red()
        )
        notfound.set_author(
            name=f"{botname}",
            icon_url=f"{icon_url}"
        )
        await ctx.send(embed=notfound, file=icon_file)
    elif isinstance(error, commands.CommandInvokeError): 
        if isinstance(error.original, discord.errors.HTTPException):
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.WARN)
            logging.warn("[WARN] Error processing http request, return code 400(Bad Request), are you using an invalid url?")
            await generic_error(ctx, icon_file, icon_url, error)
            
    elif isinstance(error, commands.BadArgument): 
        notfound = discord.Embed(
            title="Invalid argument! :scream:",
            description="You did not enter the valid type of the argument. Please try again!",
            color=discord.Color.red()
        )
        notfound.set_author(
            name=f"{botname}",
            icon_url=f"{icon_url}"
        )
        await ctx.send(embed=notfound, file=icon_file)
    else:
        await generic_error(ctx, icon_file, icon_url, error)
        print_err(error)


