import discord
from discord.ext import commands
from discord import SlashCommandGroup, option
from bot.bot import Bot
from bot.util.embed import embed_generator
from bot.views.scammerlookup import ScammerLookupView 

def data_to_string(*data):
    string = ""
    for item in data:
        if type(item) in [dict, list]:
            string += data_to_string(item)

        string += f"{item}\u200b"

class LookupModule(commands.Cog):
    def __init__(self, bot):
        self.bot:Bot = bot

    def is_match(self, scammer, arguments):
        for key, value in scammer.items():
            if isinstance(value, str) and arguments.lower() in value.lower():
                return True
            elif isinstance(value, list):
                if any(isinstance(item, str) and arguments.lower() in item.lower() for item in value):
                    return True
        return False

    scammers = SlashCommandGroup("scammers", "Scammer related commands.")

    @scammers.command(
        name="lookup",
        description="Look up a scammer by his info.",
    )
    @option(
        name="query",
        description="Text to scan the database for.",
        type=str,
        required=True,
    )
    async def lookup(self, ctx: discord.ApplicationContext, query: str):
        collection = self.bot.db["scammers"]

        data = []
        scammers_data = collection.find({})

        for scammer in scammers_data:
            if self.is_match(scammer, query):
                data.append(scammer)

        if not data:
            return await ctx.respond(embed=embed_generator(title="Scammer Lookup", description=f"No scammers found for given query: `{query}`"))

        view = ScammerLookupView(scammer_data=data)
        embed = view.generate_embed()

        await ctx.respond(embed=embed, view=view)

        


def setup(bot:Bot):
    bot.add_cog(LookupModule(bot))