import discord
from discord.ext import commands
import random
import aiohttp

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"Avatar de {member.display_name}", color=discord.Color.random())
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed(title=f"Informações do servidor {ctx.guild.name}", color=discord.Color.random())
        embed.add_field(name="ID", value=ctx.guild.id, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Criado em", value=ctx.guild.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Dono", value=ctx.guild.owner, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Membros", value=ctx.guild.member_count, inline=True)
        embed.add_field(name="Cargos", value=len(ctx.guild.roles), inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))