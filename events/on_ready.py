import discord
from dotenv import load_dotenv, find_dotenv
import os
import time

load_dotenv(find_dotenv())
uptime = time.time()
async def on_ready(bot):
    uptime = time.time()
    synced = await bot.tree.sync()
    # #for testing
    guild_id_str = os.getenv("DEFAULTGUILDID", "0")
    guildId = int(guild_id_str)
    if guildId:
        await bot.tree.sync(guild=discord.Object(id=guildId))
    print(f"Synced {len(synced)} command(s).")
    print(f"We have logged in as {bot.user}")
