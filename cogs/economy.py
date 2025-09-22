import discord
from discord.ext import commands
import random
import aiohttp
import json
import os

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'economy.json'

    def load_data(self):
        if not os.path.exists(self.data_file):
            return {}
        with open(self.data_file, 'r') as f:
            return json.load(f)

    def save_data(self, data):
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    @commands.command()
    async def balance(self, ctx):
        data = self.load_data()
        user_id = str(ctx.author.id)
        saldo = data.get(user_id, 0)
        await ctx.send(f"{ctx.author.mention}, seu saldo é de {saldo} moedas.")

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)  # 1 uso a cada 86400 segundos (24h)
    async def daily(self, ctx):
        data = self.load_data()
        user_id = str(ctx.author.id)
        saldo = data.get(user_id, 0)

        saldo += 100
        data[user_id] = saldo
        self.save_data(data)
        await ctx.send(f"{ctx.author.mention}, você recebeu 100 moedas! Agora você tem {saldo} moedas.")

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            tempo_restante = int(error.retry_after)
            horas = tempo_restante // 3600
            minutos = (tempo_restante % 3600) // 60
            segundos = int(tempo_restante % 60)
            await ctx.send(
                f"⏳ Você já usou seu daily hoje! Tente novamente em {horas}h {minutos}m {segundos}s."
            )

async def setup(bot):
    await bot.add_cog(Economy(bot))