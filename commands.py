from discord.ext import commands
from discord import app_commands
import discord
from inteligencia_artesanal import generarRespuesta
import random


class IA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="nexi")
    async def nexi(self, ctx, *, consulta: str):
        """Comando para hablar con Nexi"""
        # Ya no necesitas limpiar el texto, 'consulta' ya trae solo el mensaje
        async with ctx.typing():
            respuesta = await generarRespuesta(ctx.message, self.bot.user)
            await ctx.reply(respuesta)

    @commands.hybrid_command(name="sico")
    async def sico(self, ctx):
        """Lanzarle un tubo a otro usuario"""
        sylveon_asaltado = ctx.message.mentions[0]
        await ctx.send(
            f"¡**{ctx.author.display_name}** le ha lanzado un tubo a **{sylveon_asaltado.display_name}** rompiendole la cabeza alv!"
        )

    @commands.hybrid_command(name="hablar")
    async def hablar(self, ctx):
        """Podemos hablar ?"""
        await ctx.send("Podemos hablar? ¡Podemos hablar! ¡¡¡¡ ¡¡¡¡ ¡¡¡¡ !!!... Bueno")

    @commands.hybrid_command(name="ahi")
    async def ahi(self, ctx):
        """Inmoviliza a otro usuario"""
        sylveon_asaltado = ctx.message.mentions[0]
        await ctx.send(
            f"¡**{ctx.author.display_name}** ha inmovilizado a **{sylveon_asaltado.display_name}**\ncomo llego eso ahi :herb:?"
        )

    @commands.hybrid_command(name="detonacion")
    async def detonacion(self, ctx):
        """Detona a un usuario o se detonado"""
        resuldato_aleatorio = random.randint(1, 3)
        eevesito_obejtivo = ctx.message.mentions[0]
        if resuldato_aleatorio < 2:
            await ctx.send(
                f"intentaste detonar a **{eevesito_obejtivo.display_name}** pero te termino detonando a ti\nalch que sabroso w :fire:"
            )
        else:
            await ctx.send(
                f"**{ctx.author.display_name}** detono asi bien sabroso a **{eevesito_obejtivo.display_name}**!\nuy cuanta pasion, los ecos de la detonada resuenan en toda la habitacion :fire:"
            )

    @app_commands.command(
        name="secretear",
        description="Manda un mensaje en secreto sin que sepan q fuiste tu",
    )
    async def secretear(self, interaction: discord.Interaction, mensaje: str):
        # 1. Le avisamos al usuario que funcionó (ephemeral=True hace que solo él lo vea)
        await interaction.response.send_message(
            "Mensaje enviado de forma anónima 🤫", ephemeral=True
        )

        # 2. El bot manda el texto público al canal
        nexi_dice = generarRespuesta(
            f"Este es un mensaje secreto, da el mensaje sin revelar de quien es: [{mensaje}]"
        )
        await interaction.channel.send(nexi_dice)


# Esta función es obligatoria para que el bot pueda cargar el Cog
async def setup(bot):
    await bot.add_cog(IA(bot))
