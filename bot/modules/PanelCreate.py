import discord
from discord import SlashCommandGroup, option
from discord.ext import commands
from bot.bot import Bot
from bot.views.report import ReportView

class PanelCreate(commands.Cog):
    def __init__(self, bot):

        self.bot:Bot = bot

    panels = SlashCommandGroup("panels", "Panel creation commands")

    @panels.command(
        name="report",
        description="Creates a new panel for a reporting a scammer."
    )
    @option(
        name="channel",
        description="Channel where the panel will be created.",
        type=discord.TextChannel,
        required=True,
    )
    @commands.is_owner()
    async def panel_report(self, ctx: discord.ApplicationContext, channel: discord.TextChannel) -> None:
        view = ReportView(self.bot)
        embed = discord.Embed(
            title="Report Scammer",
            description=(
                "If you want to report a scammer, press the button below.\n\n"
                "## How to have the best chances to get someone marked?\n"
                "- gather evidence (video preferred) of you, or someone else getting scammed\n"
                "- explain in detail what happened\n"
                "**we will ask you if we find anything unclear**."
            ),
            color=discord.Color.red(),
        )
        await channel.send(embed=embed, view=view)

        await ctx.respond(f"Panel has been set up.")



def setup(bot:Bot):
    bot.add_cog(PanelCreate(bot))