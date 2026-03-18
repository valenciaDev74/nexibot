from discord.ext import commands
from discord import app_commands
import discord
from src.inteligencia_artesanal import generar_respuesta, buscar_informacion
from src import variantes
import random
import asyncio
import datetime


class IA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ------------ Comandos de texto (prefijos) ------------
    @commands.command(name="nexi")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def nexi(self, ctx, *, consulta: str):
        """Comando para hablar con Nexi"""
        async with ctx.typing():
            respuesta = await generar_respuesta(ctx.message, self.bot.user)
            await ctx.reply(respuesta)

    @commands.command(name="actually")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def actually(self, ctx, *, consulta: str):
        """Busca información en Google"""
        async with ctx.typing():
            respuesta = await buscar_informacion(ctx.message, self.bot.user)
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

    @commands.command(name="funar")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def funar(
        self,
        ctx,
        objetivo: discord.Member = None,
        *,
        razon: str = random.choice(variantes.COMANDO_FUNA_MOTIVOS_DEFAULT),
    ):
        if not objetivo:
            await ctx.send("¿A quién quieres funar, w? Menciona a alguien.")
            return

        if objetivo == ctx.author:
            await ctx.send("No te puedes funar a ti mismo, no seas payaso. 🤡")
            return

        # if objetivo == self.bot.user:
        #     await ctx.send("No te puedes funar al bot, papá. 🤖🚫")
        #     return

        # 1. Crear el Embed
        frase = random.choice(variantes.COMANDO_FUNA_SOLICITUD).format(
            autor=ctx.author.display_name,
            objetivo=objetivo.display_name,
        )

        embed = discord.Embed(
            title="🚨 ¡ALERTA DE FUNA! 🚨",
            description=f"{frase}\n\n**Razón:** {razon}\n\n*Si llegamos a 4 💀, se va al SECOT a pensar por 50s.*",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now(),
        )
        embed.set_thumbnail(url=objetivo.display_avatar.url)
        embed.set_footer(text=f"Funa iniciada por {ctx.author.display_name}")

        # 2. Enviar el mensaje y agregar la reacción inicial
        mensaje_funa = await ctx.send(embed=embed)
        await mensaje_funa.add_reaction("💀")

        # 3. Función para revisar los votos
        def check(reaction, user):
            # Que sea la calavera, en nuestro mensaje y que no cuente al bot
            return (
                str(reaction.emoji) == "💀"
                and reaction.message.id == mensaje_funa.id
                and not user.bot
            )

        try:
            # Esperamos hasta que alguien reaccione, pero lo metemos en un bucle
            while True:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=60.0, check=check
                )

                # Buscamos la reacción específica en el mensaje actualizado
                mensaje_actualizado = await ctx.channel.fetch_message(mensaje_funa.id)
                reaccion_skull = discord.utils.get(
                    mensaje_actualizado.reactions, emoji="💀"
                )

                if (
                    reaccion_skull and reaccion_skull.count >= 6
                ):  # El bot ya puso 1, así que 4 reacciones = 3 usuarios + bot
                    # 4. Aplicar el castigo (Timeout)
                    tiempo_castigo = datetime.timedelta(seconds=50)
                    try:
                        mensaje_funa_efectiva = random.choice(
                            variantes.COMANDO_FUNA_EFECTIVA
                        ).format(
                            autor=ctx.author.display_name,
                            objetivo=objetivo.display_name,
                        )
                        await objetivo.timeout(
                            tiempo_castigo, reason=f"Funa colectiva: {razon}"
                        )
                        await ctx.send(mensaje_funa_efectiva)
                    except discord.Forbidden:
                        await ctx.send("Chale, no hay webos, es admin w")
                    except Exception as e:
                        await ctx.send(f"Hubo un error al ejecutar la funa: {e}")

                    # Eliminar el mensaje de votación al aplicar la funa
                    try:
                        await mensaje_funa.delete()
                    except discord.NotFound:
                        pass
                    except Exception as e:
                        await ctx.send(f"No pude eliminar el mensaje de funa: {e}")

                    break  # Salimos del bucle una vez ejecutado

        except asyncio.TimeoutError:
            # Si pasa 1 minuto y no hay votos suficientes, la funa expira y se borra el mensaje
            try:
                await mensaje_funa.delete()
            except discord.NotFound:
                pass
            except Exception as e:
                await ctx.send(f"No pude eliminar el mensaje de funa: {e}")

            await ctx.send("La funa ha expirado por falta de pruebas (1 minuto). ⚖️")

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
