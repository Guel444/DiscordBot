import discord
from aiohttp.abc import HTTPException
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)  # Verifica permissão do autor
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(
                f'{member.display_name} foi expulso (a) do servidor.\nMotivo: {reason if reason else "Nenhum motivo informado."}')
        except discord.Forbidden:
            await ctx.send("Eu não tenho permissão para expulsar esse usuário.")
        except discord.HTTPException:
            await ctx.send("Algo deu errado ao tentar expulsar o usuário.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Você não tem permissão para usar esse comando.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Por favor, mencione o usuário que deseja expulsar.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.display_name} foi banido (a) do servidor. \nMotivo: {reason if reason else 'Nenhum motivo foi  informado.'}")
        except discord.Forbidden:
            await ctx.send('Eu não tenho permissão para banir esse usuário.')
        except discord.HTTPException:
            await ctx.send('Algo deu errado ao tentar banir o usuário.')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Você não tem permissão para banir membros.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Por favor, mencione o usuário que deseja banir.')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        mute_role = discord.utils.get(ctx.guild.roles, name='Muted')

        if not (await self.bot.is_owner(ctx.author)) and not ctx.author.guild_permissions.mute_members:
            await ctx.send("Você não tem permissão para silenciar membros.")
            return

        if not mute_role:
            mute_role = await ctx.guild.create_role(name='Muted')
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages = False, speak = False)

        if mute_role in member.roles:
            await ctx.send(f'{member.mention} já está silenciado.')
            return

        if ctx.guild.me.top_role <= mute_role:
            await ctx.send("Não consigo aplicar o cargo 'Muted'. Meu cargo está abaixo dele na hierarquia.")
            return

        try:
            await member.add_roles(mute_role, reason=reason)
            await ctx.send(f"{member.mention} foi silenciado (a) com sucesso.\nMotivo: {reason if reason else 'Nenhum motivo informado'}")
        except discord.Forbidden:
            await ctx.send('Não tenho permissão para silenciar esse membro.')
        except discord.HTTPException:
            await ctx.send('Ocorreu um erro ao silenciar esse membro.')

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Você não tem permissão para silenciar membros.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Por favor, mencione o usuário que deseja silenciar.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        try:
            user = discord.Object(id=user_id)
            await ctx.guild.unban(user)
            await ctx.send(f"Usuário com ID `{user_id}` foi desbanido com sucesso!")

        except discord.NotFound:
            await ctx.send("Esse usuário não está banido.")
        except discord.Forbidden:
            await ctx.send("Não tenho permissão para desbanir esse usuário.")
        except discord.HTTPException as e:
            await ctx.send(f"Erro ao desbanir: {e}")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Você não tem permissão para desbanir membros.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Por favor, informe o ID do usuário que deseja desbanir.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Por favor, informe um ID válido.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Muted')

        if not role:
            await ctx.send("O cargo 'Muted' não foi encontrado.")
            return

        try:
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f'{member.mention} foi desmutado com sucesso.')

            elif role not in member.roles:
                await ctx.send(f'{member.mention} não está mutado.')

        except discord.Forbidden:
                await ctx.send("Não tenho permissão para desmutar este membro.")
        except discord.HTTPException:
                await ctx.send("Ocorreu um erro ao desmutar este membro.")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Você não tem permissão para desmutar membros.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Por favor, informe o membro que deseja desmutar.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Por favor, informe um membro válido.")


async def setup(bot):
    await bot.add_cog(Moderation(bot))