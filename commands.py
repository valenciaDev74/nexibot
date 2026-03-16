from discord.ext import commands
from discord import app_commands
import discord
from inteligencia_artesanal import generarRespuesta
import variantes
import random


class IA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ------------ Comandos de texto (prefijos) ------------
    @commands.command(name="nexi")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def nexi(self, ctx, *, consulta: str):
        """Comando para hablar con Nexi"""
        async with ctx.typing():
            respuesta = await generarRespuesta(ctx.message, self.bot.user)
            await ctx.reply(respuesta)

    @commands.command(name="hablar")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def hablar(self, ctx):
        """Podemos hablar ?"""
        async with ctx.typing():
            await ctx.send(
                "Podemos hablar? ¡Podemos hablar! ¡¡¡¡ ¡¡¡¡ ¡¡¡¡ !!!... Bueno"
            )

    @commands.command(name="ahi")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ahi(self, ctx):
        """Inmoviliza a otro usuario"""
        async with ctx.typing():
            mensaje_inmovilizacion = random.choice(
                variantes.COMANDO_INMOVILIZAR
            ).format(
                autor=ctx.author.display_name,
                sylveon_asaltado=ctx.message.mentions[0].display_name,
            )
            await ctx.send(mensaje_inmovilizacion)

    @commands.command(name="sico")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sico(self, ctx):
        """Lanzarle un tubo a otro usuario"""
        async with ctx.typing():
            mensaje_psicorayo = random.choice(variantes.COMANDO_PSICORAYO).format(
                autor=ctx.author.display_name,
                sylveon_asaltado=ctx.message.mentions[0].display_name,
            )
            await ctx.send(mensaje_psicorayo)

    @commands.command(name="detonacion")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def detonacion(self, ctx):
        """Detona a un usuario o se detonado"""
        eevesito_obejtivo = ctx.message.mentions[0]
        async with ctx.typing():
            resuldato_aleatorio = random.randint(1, 3)
            if resuldato_aleatorio < 2:
                mensaje_detonacion_fallida = random.choice(
                    variantes.COMANDO_DETONACION_FALLIDA
                ).format(
                    autor=ctx.author.display_name,
                    eevesito_objetivo=eevesito_obejtivo.display_name,
                )
                await ctx.send(mensaje_detonacion_fallida)
            else:
                mensaje_detonacion_efectiva = random.choice(
                    variantes.COMANDO_DETONACION_EFECTIVA
                ).format(
                    autor=ctx.author.display_name,
                    eevesito_objetivo=eevesito_obejtivo.display_name,
                )
                await ctx.send(mensaje_detonacion_efectiva)

    # ------------ Comandos de aplicación (slash) ------------
    @app_commands.command(
        name="secretear",
        description="Manda un mensaje en secreto sin que sepan q fuiste tu",
    )
    @app_commands.checks.cooldown(1, 10, key=lambda i: i.user.id)
    async def secretear(self, interaction: discord.Interaction, mensaje: str):
        mensaje_titular = random.choice(variantes.COMANDO_MENSAJE_SECRETO)
        await interaction.channel.send(f"**{mensaje_titular}**\n{mensaje}")


# Esta función es obligatoria para que el bot pueda cargar el Cog
async def setup(bot):
    await bot.add_cog(IA(bot))
