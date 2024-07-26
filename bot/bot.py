import discord
from discord.ext import commands, tasks
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.token = os.getenv('TOKEN')

        self.owner_ids = []
        self.staff = []
        self.db = MongoClient(os.getenv('MONGODB_URI'))['scammer-list']

        self.load_modules()

    def load_modules(self):
        for file in os.listdir('bot/modules'):
            if file.endswith('.py'):
                module_name = file[:-3]
                self.load_extension(f'bot.modules.{module_name}')
                print(f'Module {module_name} loaded')


    async def on_ready(self):
        staff_collection = self.db["staff"]
        staff:list = staff_collection.find({})

        for staff_member in staff:
            if staff_member.get("owner"):
                self.owner_ids.append(staff_member['id'])
                print(f"Owner loaded: {staff_member['username']}")
            
            else:
                self.staff.append(staff_member["id"])
                print(f"Staff loaded: {staff_member['username']}")

    async def on_interaction(self, interaction: discord.Interaction):
        await interaction.response.defer()
        return await super().on_interaction(interaction)

    async def start(self):
        await super().start(self.token)

def _bot():
    bot = Bot()
    return bot