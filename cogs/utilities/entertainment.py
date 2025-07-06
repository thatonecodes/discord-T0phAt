import discord
from discord.ext import commands
from discord import app_commands
from utils import BaseClass
import random
import aiohttp

class Entertainment(BaseClass):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)

    @commands.command(name="quote", help="Get an inspirational quote")
    async def quote(self, ctx: commands.Context) -> None:
        url = "https://zenquotes.io/api/random"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        quote = data[0]["q"]
                        author = data[0]["a"]
                        await self.send_embed(
                            ctx,
                            title="💡 Inspirational Quote",
                            description=f"“{quote}”\n\n— *{author}*",
                            colour=discord.Color.green()
                        )
                    else:
                        raise Exception("API failed")
            except Exception:
                await self.send_embed(
                    ctx,
                    title="❌ Failed to fetch quote",
                    description="Please try again later.",
                    colour=discord.Color.red()
                )

    @commands.command(name="meme", help="Fetch a meme from Reddit")
    async def meme(self, ctx: commands.Context) -> None:
        url = "https://meme-api.com/gimme"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        title = data.get("title", "Meme")
                        image = data.get("url", "")
                        subreddit = data.get("subreddit", "unknown")
                        post_link = data.get("postLink", "")

                        await self.send_embed(
                            ctx,
                            title=f"🤣 {title}",
                            description=f"From r/{subreddit}\n[View Post]({post_link})",
                            thumbnail=image,
                            colour=discord.Color.orange()
                        )
                    else:
                        raise Exception("API failed")
            except Exception:
                await self.send_embed(
                    ctx,
                    title="❌ Failed to fetch meme",
                    description="Please try again later.",
                    colour=discord.Color.red()
                )

    @commands.command(name="poll", help='Create a poll. Usage: $poll "Question" "Option1" "Option2" ...')
    async def poll(self, ctx: commands.Context, question: str, *options: str) -> None:
        if len(options) < 2:
            await self.send_embed(
                ctx,
                title="❌ Poll Error",
                description="You must provide at least **2** options.",
                colour=discord.Color.red(),
            )
            return

        if len(options) > 10:
            await self.send_embed(
                ctx,
                title="❌ Poll Error",
                description="You can only provide up to **10** options.",
                colour=discord.Color.red(),
            )
            return

        emojis: list[str] = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

        description = "\n".join(
            f"{emojis[i]} {option}" for i, option in enumerate(options)
        )

        embed = discord.Embed(
            title=f"📊 {question}",
            description=description,
            color=discord.Color.blue()
        )

        url = ctx.author.avatar.url if ctx.author.avatar else self.icon_url
        embed.set_footer(text=f"Poll created by {ctx.author.display_name}", icon_url=url)
        message = await ctx.send(embed=embed)

        for i in range(len(options)):
            await message.add_reaction(emojis[i])

    @commands.command(name="dice", help="Roll a die (default 6-sided). Usage: $dice [sides]")
    async def dice(self, ctx: commands.Context, sides: int = 6) -> None:
        if sides < 1:
            await self.send_embed(
                ctx,
                title="❌ Invalid Number",
                description="Number of sides must be at least 1.",
                colour=discord.Color.red(),
            )
            return

        result: int = random.randint(1, sides)
        await self.send_embed(
            ctx,
            title="🎲 Dice Roll",
            description=f"You rolled a **d{sides}** and got **{result}**!",
            colour=discord.Color.blurple(),
        )

    @commands.command(name="rps", help="Play Rock, Paper, Scissors! Usage: $rps <rock|paper|scissors>")
    async def rps(self, ctx: commands.Context, choice: str) -> None:
        valid_choices: dict[str, str] = {
            "rock": "🪨 Rock",
            "paper": "📄 Paper",
            "scissors": "✂️ Scissors"
        }

        user_choice = choice.lower()
        if user_choice not in valid_choices:
            await self.send_embed(
                ctx,
                title="❌ Invalid Choice",
                description="Please choose one of: `rock`, `paper`, or `scissors`.",
                colour=discord.Color.red(),
            )
            return

        bot_choice: str = random.choice(list(valid_choices.keys()))

        # Determine winner
        if user_choice == bot_choice:
            result = "🤝 It's a tie!"
            color = discord.Color.gold()
        elif (
            (user_choice == "rock" and bot_choice == "scissors") or
            (user_choice == "paper" and bot_choice == "rock") or
            (user_choice == "scissors" and bot_choice == "paper")
        ):
            result = "🎉 You win!"
            color = discord.Color.green()
        else:
            result = "😢 You lose!"
            color = discord.Color.red()

        await self.send_embed(
            ctx,
            title="🪨 Rock Paper Scissors",
            description=(
                f"**You chose:** {valid_choices[user_choice]}\n"
                f"**Bot chose:** {valid_choices[bot_choice]}\n\n"
                f"**{result}**"
            ),
            colour=color,
        )
    @commands.command(name="guess", help="Guess a number between 1 and 10 - use `$guess {number: int}`")
    async def guess(self, ctx: commands.Context, number: int) -> None:
        if not 1 <= number <= 10:
            await self.send_embed(
                ctx,
                title="❌ Invalid Guess",
                description="Please guess a number between 1 and 10.",
                colour=discord.Color.red(),
            )
            return

        answer: int = random.randint(1, 10)
        if number == answer:
            message = f"🎉 Correct! The number was **{answer}**."
            color = discord.Color.green()
        else:
            message = f"😞 Nope! You guessed **{number}**, but it was **{answer}**."
            color = discord.Color.red()

        await self.send_embed(
            ctx,
            title="🎲 Number Guessing Game",
            description=message,
            colour=color,
        )

    @commands.command(name="coinflip", help="50/50 chance to get heads/tails!")
    async def coinflip(self, ctx: commands.Context) -> None:
        result: str = random.choice(["Heads", "Tails"])
        await self.send_embed(
            ctx,
            title="🪙 Coin Flip",
            description=f"The coin landed on **{result}**!",
            colour=discord.Color.gold(),
        )

    @commands.command(name="8ball", help="Magic 8-ball responses to questions - use `$8ball {question: str}`")
    async def eight_ball(self, ctx: commands.Context, *, question: str) -> None:
        responses: list[str] = [
            "Yes.", "No.", "Maybe.", "Ask again later.", "Definitely.", "I don't think so.",
            "Without a doubt.", "Very doubtful.", "Absolutely!", "Not sure about that."
        ]
        answer: str = random.choice(responses)
        await ctx.reply(f"🎱 Question: *{question}*\nAnswer: **{answer}**")

    @app_commands.command(name="joke", description="Get a random joke")
    async def joke_slash(self, interaction: discord.Interaction) -> None:
        fallback_jokes: list[tuple[str, str]] = [
            ("Why don't scientists trust atoms?", "Because they make up everything!"),
            ("What do you call fake spaghetti?", "An impasta."),
            ("Why did the scarecrow win an award?", "Because he was outstanding in his field!"),
            ("How does a penguin build its house?", "Igloos it together."),
        ]

        joke: tuple[str, str] | None = None

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://official-joke-api.appspot.com/random_joke") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        joke = (data["setup"], data["punchline"])
        except Exception:
            joke = None

        if joke is None:
            joke = random.choice(fallback_jokes)

        setup, punchline = joke
        await interaction.response.send_message(f"**{setup}**\n||{punchline}||")


async def setup(bot: commands.Bot) -> None:
    await BaseClass.setup(bot, Entertainment)
