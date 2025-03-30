import discord
from dotenv import load_dotenv, find_dotenv
import os
import time
from utils import get_logger

load_dotenv(find_dotenv())
logger = get_logger()
uptime = time.time()

async def on_ready(bot):
    uptime = time.time()
    synced = await bot.tree.sync()
    # #for testing
    guild_id_str = os.getenv("DEFAULTGUILDID", "0")
    guildId = int(guild_id_str)

    if guildId:
        await bot.tree.sync(guild=discord.Object(id=guildId))

    logger.debug(f"Synced {len(synced)} command(s).")
    logger.debug(f"We have logged in as {bot.user} at {uptime}s")
