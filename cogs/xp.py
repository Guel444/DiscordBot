# cogs/xp.py
import discord
from discord.ext import commands
import json
import os
import random

class Xp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "xp.json"
        self.xp_data = self.load_data()

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(self.file_path, "w") as f:
            json.dump(self.xp_data, f, indent=4)

    def add_xp(self, guild_id, user_id, amount):
        guild_id = str(guild_id)
        user_id = str(user_id)

        if guild_id not in self.xp_data:
            self.xp_data[guild_id] = {}

        if user_id not in self.xp_data[guild_id]:
            self.xp_data[guild_id][user_id] = {"xp": 0, "level": 1}

        self.xp_data[guild_id][user_id]["xp"] += amount

        xp = self.xp_data[guild_id][user_id]["xp"]
        level = self.xp_data[guild_id][user_id]["level"]
        next_level_xp = level * 100

        if xp >= next_level_xp:
            self.xp_data[guild_id][user_id]["level"] += 1
            self.xp_data[guild_id][user_id]["xp"] = xp - next_level_xp
            return True  # Subiu de nível

        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # XP por mensagem
        gained = random.randint(5, 15)
        leveled_up = self.add_xp(message.guild.id, message.author.id, gained)

        if leveled_up:
            await message.channel.send(f"🎉 {message.author.mention} subiu para o próximo nível!")

        self.save_data()
        # await self.bot.process_commands(message)

    @commands.command()
    async def perfil(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user_id = str(member.id)
        guild_id = str(ctx.guild.id)

        if guild_id not in self.xp_data or user_id not in self.xp_data[guild_id]:
            await ctx.send("Este usuário ainda não tem XP registrado.")
            return

        data = self.xp_data[guild_id][user_id]
        xp = data["xp"]
        level = data["level"]
        next_level = level * 100

        await ctx.send(f"📊 **{member.display_name}** está no nível **{level}** com **{xp}/{next_level} XP**.")

    @commands.command()
    async def rank(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.xp_data:
            await ctx.send("Ninguém tem XP ainda neste servidor.")
            return

        ranking = sorted(self.xp_data[guild_id].items(), key=lambda x: (x[1]["level"], x[1]["xp"]), reverse=True)
        embed = discord.Embed(title="🏆 Ranking de XP", color=discord.Color.gold())

        for i, (user_id, data) in enumerate(ranking[:10], 1):
            user = await self.bot.fetch_user(int(user_id))
            embed.add_field(
                name=f"{i}. {user.name}",
                value=f"Nível {data['level']} – {data['xp']} XP",
                inline=False
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Xp(bot))
