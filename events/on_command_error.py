import discord
from discord.ext import commands
from discord.file import File
from utils import getIcon, getName, get_logger

botname: str = getName()
logger = get_logger()

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
        logger.warn("[WARN] There was an issue with the icon file, using NO icon file.")
        await ctx.send(embed=errorembed)


def print_err(error):
    logger.error("[ERR] An error occurred during the execution of the script! Running traceback...")
    logger.error("An exception occurred: %s", error, exc_info=True)

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
            logger.warn("[WARN] Error processing http request, return code 400(Bad Request), are you using an invalid url?")
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
