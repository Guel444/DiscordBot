import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

async def main():
    await bot.load_extension('cogs.fun')
    await bot.load_extension('cogs.moderation')
    await bot.load_extension('cogs.utility')
    await bot.start("Seu_Token_Aqui")

asyncio.run(main())