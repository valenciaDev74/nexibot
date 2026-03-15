import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_GEMINI = os.getenv("API_GEMINI")
TOKEN_DISCORD = os.getenv("API_DISCORD")
print(f"TOKEN_GEMINI: {TOKEN_GEMINI}")
print(f"TOKEN_DISCORD: {TOKEN_DISCORD}")

intents = discord.Intents.default()
intents.message_content = True


class NexiBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Aquí cargamos el archivo ia_cog.py que está en la carpeta cogs
        # Se usa punto (.) en lugar de diagonal (/)
        await self.load_extension("commands")
        print("Módulo de IA cargado con éxito.")

        try:
            synced = await self.tree.sync()
            print(f"Se registraron {len(synced)} comandos pal menú, w.")
        except Exception as e:
            print(f"Chale, no se pudo sincronizar: {e}")

    async def on_ready(self):
        print(f"Nexi conectado como {self.user}")


# Ejecución del bot
bot = NexiBot()
bot.run(TOKEN_DISCORD)
