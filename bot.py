import datetime
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = 1210295265097949264
MAX_SESSION_TIME_MINUTES = 45
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")


@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Hello! Study bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    
    await channel.send("Hello! Study bot is ready!")


@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder():

    # Ignore the first execution of this command.
    if break_reminder.current_loop == 0:
        return

    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(
        f"**Take a break!** You've been studying for {MAX_SESSION_TIME_MINUTES} minutes."
    )


@bot.tree.command(description="Welcome User", name="ajeah")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"ajaeh ! {interaction.user.mention}",ephemeral=True)


@bot.command()
async def promt(ctx, *args):
    if ctx.author == bot.user:
        return
    arguments = " ".join(args)
    response = model.generate_content(arguments, stream=True)

    for chunk in response:
        await ctx.send(chunk.text)


@promt.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("I could not find that member...")


@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    break_reminder.start()
    await ctx.send(f"New session started at {human_readable_time}")


@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active!")
        return

    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()
    await ctx.send(f"Session ended after {human_readable_duration}.")


bot.run(BOT_TOKEN)
