import discord
from discord.ext import commands
from bot.bot import Bot
from bot.util.checks import is_scammer

class AppealCommand(commands.Cog):
    def __init__(self, bot):
        self.bot:Bot = bot

    @commands.slash_command(
        name="appeal",
        description="Appeals a scammer profile.",
        integration_types={discord.IntegrationType.user_install, discord.IntegrationType.guild_install}
    )
    @is_scammer()
    async def appeal(self, ctx: discord.ApplicationContext):
        ...

def setup(bot:Bot):
    bot.add_cog(AppealCommand(bot))