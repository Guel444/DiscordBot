import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

async def main():
    await bot.load_extension('cogs.fun')
    await bot.load_extension('cogs.moderation')
    await bot.load_extension('cogs.utility')
    await bot.load_extension('cogs.economy')
    await bot.load_extension('cogs.xp')
    await bot.start("Seu_Token")

asyncio.run(main())