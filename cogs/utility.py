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

    @commands.command(name='help')
    async def help_user(self, ctx):
        embed = discord.Embed(title="Comandos disponíveis", color=discord.Color.random())
        embed.add_field(name="!ping", value="Responde pong...", inline=False)
        embed.add_field(name="!falar", value="O bot repete o que você escrever (comando de fala).", inline=False)
        embed.add_field(name="!piada", value="Envia uma piada aleatória para animar o chat.", inline=False)
        embed.add_field(name="!d20", value="Rola um dado de 20 lados (D20).", inline=False)
        embed.add_field(name="!moeda", value="Joga uma moeda: cara ou coroa.", inline=False)
        embed.add_field(name="!8ball", value="Responde perguntas aleatórias com estilo místico.", inline=False)
        embed.add_field(name="!gaymetro", value="Mede (de forma brincalhona) o nível de 'gayzice' de alguém.", inline=False)
        embed.add_field(name="!qi", value="Mede (de forma engraçada) o QI de um usuário.", inline=False)
        embed.add_field(name="!trivia", value="Faz uma pergunta de trivia para desafiar os usuários.", inline=False)
        embed.add_field(name="!meme", value="Envia um meme aleatório.", inline=False)
        embed.add_field(name="!avatar", value="Mostra o avatar de um usuário mencionado.", inline=False)
        embed.add_field(name="!ship", value="Combina dois usuários e calcula a compatibilidade amorosa.", inline=False)
        embed.add_field(name="!daily", value="Coleta sua recompensa diária (sistema de economia).", inline=False)
        embed.add_field(name="!balance", value="Mostra seu saldo atual (sistema de economia).", inline=False)
        embed.add_field(name="!kick", value="Expulsa um membro do servidor (necessita permissão).", inline=False)
        embed.add_field(name="!ban", value="Bane um membro do servidor (necessita permissão).", inline=False)
        embed.add_field(name="!mute", value="Silencia um usuário no servidor (necessita permissão).", inline=False)
        embed.add_field(name="!unban", value="Desbane um usuário pelo nome ou ID.", inline=False)
        embed.add_field(name="!serverinfo", value="Mostra informações sobre o servidor.", inline=False)
        embed.add_field(name="!unmute", value="Remove o silêncio de um usuário.", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))