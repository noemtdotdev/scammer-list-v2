import discord
from discord.ext import commands, tasks
import os

from dotenv import load_dotenv
from pymongo import MongoClient
import aiohttp

load_dotenv()

class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.token = os.getenv('TOKEN')

        self.owner_ids = []
        self.staff = []
        self.db = MongoClient(os.getenv('MONGODB_URI'))['scammer-list']
        self.session = None

        self.load_modules()

    def load_modules(self):
        for file in os.listdir('bot/modules'):
            if file.endswith('.py'):
                module_name = file[:-3]
                self.load_extension(f'bot.modules.{module_name}')
                print(f'Module {module_name} loaded')

    @tasks.loop(seconds=60)
    async def load_staff(self):
        staff_collection = self.db["staff"]
        staff:list = staff_collection.find({})

        self.owner_ids = self.owner_ids[:1:]
        self.staff = []

        for staff_member in staff:
            if staff_member.get("owner"):
                if staff_member['id'] not in self.owner_ids:
                    self.owner_ids.append(staff_member['id'])
            
            else:
                self.staff.append(staff_member["id"])

    @tasks.loop(seconds=10)
    async def update_activity(self):
        scammers_collection = self.db["scammers"]
        scammers_count = scammers_collection.count_documents({})

        activity = discord.CustomActivity(f"{scammers_count} scammers | by @nom")
        await self.change_presence(activity=activity)


    @tasks.loop(hours=24)
    async def update_scammers(self):
        scammers = self.db["scammers"]
        scammers_list = scammers.find({})

        print("Starting Scammer Update")

        for scammer in scammers_list:

            user_id = int(scammer["id"])

            name_history = scammer["previous_aliases"]
            if not name_history:
                name_history = []

            current_username = scammer["username"]
            if "deleted_user" in current_username:
                continue

            if "deleted_user" in name_history:
                continue

            scammer_object = self.get_user(user_id)
            if not scammer_object:

                try:
                    scammer_object = await self.fetch_user(user_id)

                except discord.errors.NotFound:
                    scammer["username"] = name_history[-1] if len(name_history) > 0 else "deleted_user"
                    name_history.append("deleted_user")

                    scammer["previous_aliases"] = name_history

                    scammers.update_one({"id": user_id}, {"$set": scammer})
                    continue
            
            if not scammer_object:
                continue

            username = scammer_object.name

            if current_username != username:
                scammer["username"] = username
                name_history.append(current_username)

                scammer["previous_aliases"] = name_history

            scammers.update_one({"id": user_id}, {"$set": scammer})

        print("Scammer Update Complete")

    async def on_ready(self):
        self.session = aiohttp.ClientSession()
        async with self.session.get(f"{os.getenv('API_URL')}:1337/accounts") as resp:
            data = await resp.json()

            current_account = int(data["current"])
            self.owner_ids.append(current_account)

        self.load_staff.start()
        # self.update_scammers.start()
        self.update_activity.start()
        print(f'Bot is ready. Owner IDs: {self.owner_ids}')

    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.application_command:
            await interaction.response.defer()

        return await super().on_interaction(interaction)

    async def start(self):
        await super().start(self.token)

def bot():
    bot = Bot()
    return bot