import discord
from discord.ui import View, button, Modal
from bot.bot import Bot
from datetime import datetime
from bot.views.ticket import TicketView

class ReportModal(Modal):
    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, title="Report User", custom_id="report_modal")
        self.bot:Bot = bot

        self.add_item(
            discord.ui.InputText(label="User ID", placeholder="User ID of the scammer", max_length=20, min_length=18),
        )
        self.add_item(
            discord.ui.InputText(label="Reason", placeholder="How did the person scam?", style=discord.InputTextStyle.long, max_length=100),
        )
        self.add_item(
            discord.ui.InputText(label="Amount", placeholder="How much were you scammed for?", max_length=20),
        )

    def get_overwrites(self, interaction: discord.Interaction) -> dict:
        return {
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True,
                                                          read_message_history=True, view_channel=True,
                                                          embed_links=True, attach_files=True,
                                                          use_external_emojis=True, add_reactions=True,
                                                          use_application_commands=True),
        }
    
    async def callback(self, interaction: discord.Interaction) -> None:
        user_id = self.children[0].value
        reason = self.children[1].value
        amount = self.children[2].value

        collection = self.bot.db["tickets"]

        user_ticket = collection.find_one({"user_id": interaction.user.id, "closed": False})
        if user_ticket:
            await interaction.respond(f"You already have a ticket open. <#{user_ticket['channel_id']}>", ephemeral=True)
            return

        if not user_id.isdigit():
            await interaction.respond("Invalid User ID. Please provide a valid user ID.", ephemeral=True)
            return
        
        category: discord.CategoryChannel = interaction.guild.get_channel(1266768274851631307)
        if len(category.channels) == 50:
            await interaction.respond("Cannot open a new ticket as the category limit was reached. Please DM a staff member.", ephemeral=True)
            return
        
        channel = await category.create_text_channel(name=f"report-{interaction.user.name}", overwrites=self.get_overwrites(interaction))
        data = {
            "user_id": interaction.user.id,
            "channel_id": channel.id,
            "reported_user": user_id,
            "reason": reason,
            "amount": amount,
            "report_date": int(datetime.now().timestamp()),
            "closed": False
        }

        collection.insert_one(data)

        embed = discord.Embed(
            title=f"Ticket Report - {interaction.user.name}",
            description=f"User ID: `{user_id}`\nReason: `{reason}`\nAmount Scammed: `{amount}`",
            timestamp=datetime.now(),
            color=discord.Color.red(),
        )
        await channel.send(embed=embed, content=f"{interaction.user.mention}, please wait for our <@&1266760162153074740> to handle this report!", view=TicketView(self.bot))

        try:
            user = await self.bot.fetch_user(int(user_id))
            embed = discord.Embed(
                title="User Information",
                description=(
                    f"Username: **{user}**\n"
                    f"User ID: **{user.id}**\n"
                    f"Created At: **<t:{int(user.created_at.timestamp())}>**"
                ),
                color=discord.Color.red(),
            )
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            await channel.send(embed=embed)

        except discord.errors.NotFound:
            pass

        await interaction.respond(f"Your ticket has been opened, you can find it [here]({channel.jump_url})!", ephemeral=True)



class ReportView(View):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs, timeout=None)

        self.bot:Bot = bot

    @button(label="Report Someone", style=discord.ButtonStyle.red, row=0, custom_id="open_ticket")
    async def open_ticket(self, button: discord.Button, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(ReportModal(self.bot))

