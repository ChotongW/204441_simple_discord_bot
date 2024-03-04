import datetime
from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
from dotenv import load_dotenv
import os
import google.generativeai as genai
import yfinance as yf
import matplotlib.pyplot as plt
import io

from function import upcoming
from Pagination import PaginationView

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = 1210295265097949264
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PORT = os.getenv("PORT")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")


@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Hello! Study bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)

    await channel.send("Hello! Study bot is ready!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("I do not have this command.")


@bot.tree.command(description="Welcome User", name="ajeah")
async def hello_personal(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"ajaeh ! {interaction.user.mention}", ephemeral=True
    )


@bot.command()
async def hello(ctx):
    if ctx.author == bot.user:
        return
    await ctx.send("ajeah")


## show coming up anime
@bot.command(name="comingup")
async def paginate(ctx):
    data = upcoming()

    pagination_view = PaginationView()
    pagination_view.data = data
    await pagination_view.send(ctx)


@bot.command()
async def promt(ctx, *args):
    if ctx.author == bot.user:
        return
    arguments = " ".join(args)
    response = model.generate_content(arguments, stream=True)

    for chunk in response:
        await ctx.send(chunk.text)


@bot.command()
async def status(ctx, num: int):

    numbers = [
        100,
        101,
        102,
        103,
        200,
        201,
        202,
        203,
        204,
        205,
        206,
        207,
        208,
        218,
        226,
        300,
        301,
        302,
        303,
        304,
        305,
        306,
        307,
        308,
        400,
        401,
        402,
        403,
        404,
        405,
        406,
        407,
        408,
        409,
        410,
        411,
        412,
        413,
        414,
        415,
        416,
        417,
        418,
        419,
        420,
        421,
        422,
        423,
        424,
        425,
        426,
        428,
        429,
        430,
        431,
        440,
        444,
        449,
        450,
        451,
        460,
        463,
        464,
        494,
        495,
        496,
        497,
        498,
        499,
        500,
        501,
        502,
        503,
        504,
        505,
        506,
        507,
        508,
        509,
        510,
        511,
        520,
        521,
        522,
        523,
        524,
        525,
        526,
        527,
        529,
        530,
        561,
        598,
        599,
        999,
    ]
    if num in numbers:
        image_url = f"https://http.dog/{num}.jpg"
        # await ctx.send(f"Here's an image:", image_url)
        await ctx.send(image_url)


@Bot.command()
async def stock(ctx, symbol):
    try:
        stock_data = yf.download(symbol, period="1mo", interval="1d")

        plt.figure(figsize=(10, 5))
        plt.plot(stock_data["Close"], label="Close Price")
        plt.xlabel("Time (UTC-4/EDT)")
        plt.ylabel("Price (USD)")
        plt.title(f"{symbol} Stock Price (1 month)")
        plt.legend()

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        await ctx.send(file=discord.File(buffer, filename="plot.png"))
    except Exception as e:
        await ctx.send(f"Error fetching or plotting data: {e}")


@promt.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("I could not find that member...")


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
