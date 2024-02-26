import datetime
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
from dotenv import load_dotenv
import os
import google.generativeai as genai

# from flask import Flask
# import threading

# import signal


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = 1210295265097949264
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PORT = os.getenv("PORT")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")

# app = Flask(__name__)


@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()


# @app.route("/")
# def index():
#     return {"res": "bot is running"}


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Hello! Study bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)

    await channel.send("Hello! Study bot is ready!")


@bot.tree.command(description="Welcome User", name="ajeah")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"ajaeh ! {interaction.user.mention}", ephemeral=True
    )


@bot.command()
async def hello(ctx):
    if ctx.author == bot.user:
        return
    await ctx.send("ajeah")


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


# def bot_thread(func):
#     thread = threading.Thread(target=func)
#     print("Start Separate Thread")
#     thread.start()


# def run():
#     bot.run(BOT_TOKEN)


if __name__ == "__main__":
    # bot_thread(func=run)
    bot.run(BOT_TOKEN)
# def run_flask():
#     app.run()


# def stop_services(signum, frame):
#     print("Stopping services...")
#     break_reminder.stop()
#     bot.close()
#     print("Services stopped.")
#     os._exit(0)


# if __name__ == "__main__":
#     flask_thread = threading.Thread(target=run_flask)
#     flask_thread.start()
#     signal.signal(signal.SIGINT, stop_services)  # Register signal handler for Ctrl+C
#     bot.run(BOT_TOKEN)
