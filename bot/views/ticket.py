import discord
from discord.ui import View, button, Button
from bot.bot import Bot
from chat_exporter.construct.transcript import Transcript

class TicketView(View):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs, timeout=None)

        self.bot:Bot = bot

    @button(label="Close Ticket", style=discord.ButtonStyle.red, row=0, custom_id="close_ticket")
    async def close_ticket(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        with open(f"api/templates/{interaction.channel.name}-{interaction.channel.id}.html", "wb") as f:
            transcript = (
                await Transcript(
                    channel=interaction.channel,
                    limit=None,
                    messages=None,
                    pytz_timezone="UTC",
                    military_time=True,
                    fancy_times=True,
                    before=None,
                    after=None,
                    support_dev=True,
                    bot=self.bot,
                    attachment_handler=self.bot.file_handler,
                ).export()
            ).html
            f.write(transcript.encode())


        collection = self.bot.db["tickets"]
        ticket_id = interaction.channel.id

        collection.update_one({"channel_id": ticket_id}, {"$set": {"closed": True}})
        ticket_data = collection.find_one({"channel_id": ticket_id})

        url = f"https://pixly.noemt.dev/transcript/{interaction.channel.name}-{interaction.channel.id}.html"
        channel = interaction.guild.get_channel(1266773009059020913)
        embed = discord.Embed(
            title="Report Log",
            description=f"""
Opened by: <@{ticket_data['user_id']}>
Closed by: {interaction.user.mention}

Reported User: <@{ticket_data['reported_user']}>
accused of: `{ticket_data['reason']}` 
with `{ticket_data['amount']}` scammed.

Opened on: <t:{ticket_data['report_date']}>""",
            color=discord.Color.red()
        )
        view = View()
        view.add_item(Button(label="View Transcript", url=url))
        await channel.send(embed=embed, view=view)

        await interaction.channel.delete()
