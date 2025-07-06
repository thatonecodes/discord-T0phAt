import hashlib
import discord
from utils import BaseClass
import aiohttp
import base64
from discord.ext import commands

class Tools(BaseClass):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)

    @commands.command(name="hash", help="Generate MD5 and SHA256 hashes of a given input")
    async def hash(self, ctx: commands.Context, *, text: str) -> None:
        md5_hash: str = hashlib.md5(text.encode()).hexdigest()
        sha256_hash: str = hashlib.sha256(text.encode()).hexdigest()

        await self.send_embed(
            ctx,
            title="🔑 Hash Generator",
            description=f"**Input:** `{text}`",
            fields=[
                {"name": "🔒 MD5", "value": f"`{md5_hash}`", "inline": False},
                {"name": "🔐 SHA256", "value": f"`{sha256_hash}`", "inline": False},
            ],
            colour=discord.Color.purple()
        )
    
    @commands.command(name="base64encode", help="Encode the given string to base64 - use `$base64encode [message]`")
    async def base64_encode(self, ctx: commands.Context, *, text: str) -> None:
        b = base64.b64encode(bytes(text, 'utf-8')) # bytes
        base64_str = b.decode('utf-8') # convert bytes to string

        await self.send_embed(
            ctx,
            title="🖥️ base64 Encoder",
            description=f"**Input:** `{text}`",
            fields=[
                {"name": "🔒 base64", "value": f"```{base64_str}```", "inline": False},
            ],
            colour=discord.Color.purple()
        )

    @commands.command(name="base64decode", help="Decode the given string from base64 - use `$base64decode [message]`")
    async def base64_decode(self, ctx: commands.Context, *, text: str) -> None:
        try:
            decoded_bytes = base64.b64decode(text, validate=True)  # Validate input
            decoded_str = decoded_bytes.decode('utf-8')
        except Exception:
            await self.send_embed(
                ctx,
                title="❌ Invalid base64 input",
                description="Please provide a valid base64-encoded string.",
                colour=discord.Color.red()
            )
            return

        await self.send_embed(
            ctx,
            title="🖥️ Base64 Decoder",
            description=f"**Input:** `{text}`",
            fields=[
                {"name": "📝 Decoded Text", "value": f"```{decoded_str}```", "inline": False},
            ],
            colour=discord.Color.purple()
        )

    @commands.command(name="shorten", help="Shorten a URL using tinyurl.com")
    async def shorten(self, ctx: commands.Context, url: str) -> None:
        api_url = f"http://tinyurl.com/api-create.php?url={url}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url) as resp:
                    if resp.status == 200:
                        short_url = await resp.text()
                        await self.send_embed(
                            ctx,
                            title="🔗 URL Shortener",
                            description=f"Original URL:\n{url}\n\nShortened URL:\n{short_url}",
                            colour=discord.Color.blurple(),
                        )
                    else:
                        raise Exception("Failed to shorten URL")
            except Exception:
                await self.send_embed(
                    ctx,
                    title="❌ URL Shortening Failed",
                    description="Please check the URL and try again later.",
                    colour=discord.Color.red(),
                )
