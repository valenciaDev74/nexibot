import os
import webserver
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
from discord.ext import tasks

load_dotenv()


class NexiBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    @tasks.loop(minutes=20)  # Cambia cada 5 minutos
    async def cambiar_status(self):
        frases = [
            "a doblar Eevee Squad w",
            "con una tortilla de harina",
            "Deltarune (cap 5 real)",
            "a que me den un tubazo",
            "a ser un femboy god",
            "soy tu papá w",
        ]
        # Elegimos una actividad aleatoria
        nueva_actividad = discord.Game(name=random.choice(frases))
        await self.change_presence(activity=nueva_actividad)

    async def setup_hook(self):
        # Asegúrate de que el archivo se llame commands.py
        await self.load_extension("commands")

        try:
            await self.tree.sync()
            print("Slash commands sincronizados.")
        except Exception as e:
            print(f"Error sincronizando: {e}")

    async def on_ready(self):
        self.cambiar_status.start()
        print(f"Nexi listo en: {self.user}")


async def main():
    bot = NexiBot()
    async with bot:
        # Usamos el token del .env
        await bot.start(os.getenv("API_DISCORD"))


if __name__ == "__main__":
    try:
        webserver.keep_alive()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot apagado por el usuario, w.")
