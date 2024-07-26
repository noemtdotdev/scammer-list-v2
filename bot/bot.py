import discord
from discord.ext import commands
import os

from dotenv import load_dotenv

load_dotenv()

class Bot(commands.AutoShardedBot):
    def __init__(self, mongodb_connection, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.token = os.getenv('TOKEN')
        self.db = mongodb_connection

        self.owner_ids = []
        self.staff = []

        self.load_modules()

    def load_modules(self):
        for file in os.listdir('bot/modules'):
            if file.endswith('.py'):
                module_name = file[:-3]
                self.load_extension(f'bot.modules.{module_name}')
                print(f'Module {module_name} loaded')


    async def on_ready(self):
        # do some stuff to get owners and staff
        ...

    async def on_interaction(self, interaction: discord.Interaction):
        await interaction.response.defer()
        return await super().on_interaction(interaction)

    async def start(self):
        await super().start(self.token)

def _bot(mongodb_connection):
    bot = Bot(mongodb_connection)
    return bot