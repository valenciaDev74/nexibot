import os
import webserver
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class NexiBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Asegúrate de que el archivo se llame commands.py
        await self.load_extension("commands")

        try:
            await self.tree.sync()
            print("Slash commands sincronizados.")
        except Exception as e:
            print(f"Error sincronizando: {e}")

    async def on_ready(self):
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
