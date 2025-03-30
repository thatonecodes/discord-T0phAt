from typing import Dict, List
from utils import BaseClass
from discord.ext import commands
import discord
import requests
import asyncio
import aiohttp
import os
import random
import tempfile
from bs4 import BeautifulSoup

class Crawler(BaseClass):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    @commands.command(name="crawlsite", help="HTTP GET a specified site's data. - `$crawlsite (url)`")
    async def crawlsite(self, ctx, url: str):
        temp_file_path = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    html = await response.text()

                    soup = BeautifulSoup(html, "html.parser")
                    pretty_html = soup.prettify()

                    # Offload file writing to a separate thread - no blocking threads
                    temp_file_path = await asyncio.to_thread(self.write_temp_file, pretty_html)

                    await ctx.send(file=discord.File(temp_file_path, filename="response.html"))

        except aiohttp.ClientError as e:
            await self.send_embed(
                ctx,
                title="Error, ClientError!",
                description=f"Failed to retrieve data from GET request.\n\n{e}",
                colour=discord.Color.red()
            )
        except Exception as e:
            await self.send_embed(
                ctx,
                title="Something went wrong...",
                description=f"Unable to retrieve any data from GET request.\n\n{e}",
                colour=discord.Color.red()
            )

        finally:
            if temp_file_path:
                try:
                    os.remove(temp_file_path)
                except FileNotFoundError:
                    pass

    def write_temp_file(self, pretty_html: str) -> str:
        """Write the HTML content to a temporary file and return its path."""
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".html") as temp_file:
            temp_file.write(pretty_html)
            return temp_file.name

    async def maketopggrequest(self, ctx, url, params, send_embed=True):
        headers = {
            "Authorization": str(os.getenv("TOPGGAPIKEY"))
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()  # Parse the JSON response

            fields: List[Dict] = []

            for bot in data["results"]:
                description = f"""Bot ID: {bot['id']}
                Short Description: {bot['shortdesc']}
                Invite Link: {bot['invite']}
                Website: {bot['website']}"""
                fields.append({"name": bot["username"], "value": description})

            if send_embed:
                await self.send_embed(
                    ctx,
                    title=f"Get bot(s) - Limit {params['limit']}",
                    description="",
                    fields=fields
                )
            return fields
                
        else:
            if send_embed:
                await self.send_embed(
                    ctx,
                    title="Error failed to fetch",
                    description=f"Failed to fetch data. Status code: {response.status_code}"
                )
            return None

    @commands.command(name="getbots", help="Command that gets latest bots using the top.gg API (default limit 15) - `$getbots (optional limit int)`")
    async def getbots(self, ctx, optlimit=15):
        url = "https://top.gg/api/bots"
        try: 
            params = {
                "limit": int(optlimit),  # Number of bots to return
                "offset": 0,  # Skip 0 bots
                "sort": "-date",  # Sort by date in descending order
                "fields": "id,username,shortdesc,invite,website",  # Fields to return in the response
            }
        except ValueError:
            raise commands.BadArgument("Expected an integer when converting limit!")

        await self.maketopggrequest(ctx, url, params)

    @commands.command(name="getrandbot", help="Get a singular random bot from the top.gg API. - `$getrandbot`")
    async def getrandbot(self, ctx):
        url = "https://top.gg/api/bots"
        params = {
            "limit": 1, 
            "offset": random.randint(1, 1000),  # Skip random amount for a random bot 
            "sort": "-date",  # Sort by date in descending order
            "fields": "id,username,shortdesc,invite,website",  # Fields to return in the response
        }

        await self.maketopggrequest(ctx, url, params)

    async def getbotfromid(self, ctx, botId):
        try:
            user_id = int(botId)
            user = await self.bot.fetch_user(user_id)
        except discord.NotFound:
            await self.send_embed(ctx, title="User not found!", description="HTTP request returned 404 Not Found!", colour=discord.Color.red())
            return
        except discord.HTTPException:
            await self.send_embed(ctx, title="Failed to fetch user information", description="Whoops! We couldn't process that. 500 - Internal Server Error.", colour=discord.Color.red())
            return

        params = {
            "sort": "-date",  # Sort by date in descending order
            "fields": "id,username,shortdesc,invite,website",  # Fields to return in the response
        }
        url = f"https://top.gg/api/bots/{botId}"
        fields = await self.maketopggrequest(ctx, url, params, send_embed=False)

        await self.send_embed(
            ctx, 
            title=f"Info for {user.name} from top.gg",
            description="",
            fields=fields
        )

        return fields

# Setup the cog
async def setup(bot):
    await BaseClass.setup(bot, Crawler)
