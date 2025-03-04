from utils import BaseClass 
import discord
import yt_dlp
import traceback
from discord.ext import commands

class MusicPlayer(BaseClass):
    def __init__(self, bot) -> None:
        super().__init__(bot)
        if not discord.opus.is_loaded():
            opus_path = "./.venv/lib/python3.11/site-packages/discord/bin/libopus-0.x86.dll"
            discord.opus.load_opus(opus_path)

    @commands.command(help="Connect to vc you are in.")
    async def connect(self, ctx):
        try:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                await channel.connect()
                await self.send_embed(
                    ctx,
                    title=f"Joined {channel}",
                    description=f"Joined {ctx.author} in {channel}."
                )
            else:
                await self.send_embed(
                    ctx,
                    title=f"Error Joining!",
                    description=f"You need to be in a voice channel to use this command!",
                    colour=discord.Colour.red(),
                )
        except Exception as e:
            print(e)

    @commands.command(help="Tells what the bot should play. takes as URL. - use `$play URL`")
    async def play(self, ctx, url: str):
        if not ctx.voice_client:
            await ctx.invoke(self.connect)

        vc = ctx.voice_client

        if not vc:
            await self.send_embed(
                ctx,
                title="Error!",
                description="Bot is not connected to a voice channel.",
                colour=discord.Colour.red(),
            )
            return

        # YT-DLP options
        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'extract_flat': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                if info is None:
                    await self.send_embed(
                        ctx,
                        title="Error!",
                        description="Error getting youtubeDL data.",
                        colour=discord.Colour.red(),
                    )
                    return
                url2 = info['url']
                title = info.get('title', 'Unknown Title')
            except Exception as e:
                await self.send_embed(
                    ctx,
                    title="Error Playing Audio!",
                    description=f"Could not process the URL. Error: {e}",
                    colour=discord.Colour.red(),
                )
                return

        # Play audio
        try:
            vc.stop()  # Stop the current audio if playing
            vc.play(discord.FFmpegPCMAudio(url2), after=lambda e: print(f"Error: {e}" if e else None))
            await self.send_embed(
                ctx,
                title="Now Playing",
                description=f"Playing: {title}"
            )
        except Exception as e:
            print(traceback.print_exc())
            print(e)
            await self.send_embed(
                ctx,
                title="Error Playing Audio!",
                description=f"An error occurred while trying to play audio. Error: {e}",
                colour=discord.Colour.red(),
            )

    @commands.command(help="Disconnect from the vc you are in.")
    async def disconnect(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await self.send_embed(
                ctx,
                title=f"Disconnected!",
                description=f"Successfully disconnected from your current voice chat."
            )
        else:
            await self.send_embed(
                ctx,
                title=f"Error Disconnecting!",
                description=f"You need to be in a voice channel to use this command!",
                colour=discord.Colour.red(),
            )

async def setup(bot):
    await BaseClass.setup(bot, MusicPlayer)
