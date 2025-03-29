from utils import BaseClass
import discord
from discord.ext import commands

class ModerationTools(BaseClass):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    @commands.command(help="Deletes messages to clear the channel like the UNIX 'cls' command. (1000 msg default)")
    @commands.has_permissions(manage_messages=True)  # Ensure only users with the correct permissions can use it
    async def cls(self, ctx, amount: int = 1000):
        deleted_messages = await ctx.channel.purge(limit=amount)

        await self.send_embed(
                ctx,
                title="Success",
                colour=discord.Color.green(),
                description=f"✅ Cleared {len(deleted_messages)} messages!",
                ephemeral=True
        )

    @commands.command(help="Ban a user from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await self.send_embed(
            ctx,
            title="User Banned",
            description=f"🚫 {member.mention} has been banned. Reason: {reason}",
            colour=discord.Color.red()
        )

    @commands.command(help="Unban a user by ID.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await self.send_embed(
            ctx,
            title="User Unbanned",
            description=f"✅ {user.mention} has been unbanned.",
            colour=discord.Color.green()
        )

    @commands.command(help="Kick a user from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await self.send_embed(
            ctx,
            title="User Kicked",
            description=f"👢 {member.mention} has been kicked. Reason: {reason}",
            colour=discord.Color.orange()
        )

    @commands.command(help="Mute a user in voice channels.")
    @commands.has_permissions(mute_members=True)
    async def mute(self, ctx, member: discord.Member):
        await member.edit(mute=True)
        await self.send_embed(
            ctx,
            title="User Muted",
            description=f"🔇 {member.mention} has been muted in voice channels.",
            colour=discord.Color.red()
        )

    @commands.command(help="Unmute a user in voice channels.")
    @commands.has_permissions(mute_members=True)
    async def unmute(self, ctx, member: discord.Member):
        await member.edit(mute=False)
        await self.send_embed(
            ctx,
            title="User Unmuted",
            description=f"🔊 {member.mention} has been unmuted in voice channels.",
            colour=discord.Color.green()
        )

    @commands.command(help="Deafen a user in voice channels.")
    @commands.has_permissions(deafen_members=True)
    async def deafen(self, ctx, member: discord.Member):
        await member.edit(deafen=True)
        await self.send_embed(
            ctx,
            title="User Deafened",
            description=f"🔕 {member.mention} has been deafened in voice channels.",
            colour=discord.Color.red()
        )

    @commands.command(help="Undeafen a user in voice channels.")
    @commands.has_permissions(deafen_members=True)
    async def undeafen(self, ctx, member: discord.Member):
        await member.edit(deafen=False)
        await self.send_embed(
            ctx,
            title="User Undeafened",
            description=f"🔉 {member.mention} has been undeafened in voice channels.",
            colour=discord.Color.green()
        )

async def setup(bot):
    await BaseClass.setup(bot, ModerationTools)
