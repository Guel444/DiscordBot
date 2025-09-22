import discord
from discord.ext import commands
import random
import aiohttp

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

    @commands.command()
    async def falar(self, ctx, *, texto):
        await ctx.message.delete()
        await ctx.send(texto)

    @commands.command()
    async def piada(self, ctx):
        piadas = [
            "Por que o programador sempre confunde Halloween com Natal? Porque OCT 31 == DEC 25.",
            "O que o Java disse para o C? Você tem muitos problemas de ponteiro.",
            "Qual é o cúmulo da programação? Escrever um bug que se corrige sozinho.",
            "Por que o livro de matemática estava triste? Porque ele tinha muitos problemas.",
            "Por que o computador foi ao médico? Porque ele estava com um vírus!",
            "Qual é o animal mais antigo do mundo? A zebra, porque ela é em preto e branco.",
            "Por que o Wi-Fi terminou com o roteador? Porque ele encontrou uma conexão melhor.",
            "Por que o Jedi foi para a terapia? Porque ele tinha problemas com o lado sombrio."
        ]
        resposta = random.choice(piadas)
        await ctx.send(resposta)

    @commands.command()
    async def d20(self, ctx):
        resultado = random.randint(1, 20)
        await ctx.send(f"O resultado do dado é: {resultado}")

    @commands.command()
    async def moeda(self, ctx):
        resultado = random.choice(["Cara", "Coroa"])
        await ctx.send(f"O resultado é: {resultado}")

    @commands.command(name='8ball')
    async def magic_8ball(self, ctx, *, pergunta):
        respostas = [
            'Sim',
            "Não",
            'Com certeza',
            'Nunca',
            'Talvez',
            'Nem sonhando',
            'Melhor não te dizer...',
            'Você não merece ouvir a resposta'
        ]
        resposta = random.choice(respostas)
        await ctx.reply(resposta)

    @magic_8ball.error
    async def magic_8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Por favor, faça uma pergunta.")

    @commands.command()
    async def gaymetro(self, ctx, member: discord.Member):
        gay = random.randint(0, 100)
        await ctx.send(f'{member.display_name} é {gay}% gay')

    @commands.command()
    async def qi(self, ctx, member: discord.Member):
        qi = random.randint(0, 200)
        await ctx.send(f'{member.display_name} tem {qi} de QI!')

    @commands.command()
    async def trivia(self, ctx):
        perguntas = [
            "Em que ano foi lançado o primeiro filme da série “Star Wars”?",
            "Qual linguagem de programação é conhecida por seu símbolo de uma cobra?",
            "Quem é o autor da série de livros “O Senhor dos Anéis”?",
            "Qual planeta é conhecido como o “Planeta Vermelho”?",
            "Qual elemento químicos tem o símbolo “Fe”?",
            "Qual é o maior planeta do nosso sistema solar?",
            "Quem pintou a Mona Lisa?",
            "Qual é o nome da capital da Austrália?",
            "Qual é o maior órgão do corpo humano?"
            "Qual é a fórmula química da água?"
        ]

        pergunta = random.choice(perguntas)

        await ctx.send(pergunta)

    @commands.command()
    async def ship(self, ctx, member1: discord.Member, member2: discord.Member):
        ship = random.randint(0, 100)
        await ctx.send(f'{member1.display_name} e {member2.display_name} são {ship}% compatíveis!')

    @commands.command()
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://meme-api.com/gimme') as response:
                if response.status != 200:
                    await ctx.send("Não consegui pegar um meme agora. Tenta de novo mais tarde!")
                    return
                data = await response.json()
                meme_url = data.get('url')
                title = data.get('title')
                subreddit = data.get('subreddit')

                embed = discord.Embed(title=title, description=f"r/{subreddit}", color=discord.Color.random())
                embed.set_image(url=meme_url)
                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
