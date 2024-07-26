import discord
from discord.ui import View, Button, Select, Modal

class ScammerLookupView(View):
    def __init__(self, scammer_data: list[dict], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.scammer_data = scammer_data
        self.page = 0
        self.pages = (len(scammer_data) + 9) // 10

        self.add_item(self.create_prev_button())
        self.add_item(self.create_next_button())
        self.add_item(self.create_select_menu())

    def create_prev_button(self) -> Button:
        button = Button(label="Previous", style=discord.ButtonStyle.red, row=0)
        button.callback = self.previous_button
        return button

    def create_next_button(self) -> Button:
        button = Button(label="Next", style=discord.ButtonStyle.red, row=0)
        button.callback = self.next_button
        return button

    def create_select_menu(self) -> Select:
        select_menu = Select(
            placeholder="Select a Scammer",
            options=self.generate_select_menu_options(),
            row=1
        )
        select_menu.callback = self.select_menu_callback
        return select_menu

    def generate_data_embed(self, data: dict) -> discord.Embed:

        previous_aliases = "\n".join(f"{i+1}: `{alias}`" for i, alias in enumerate(data.get('previous_aliases')))

        description = (
            f"Username: `{data['username']}` {'Perhaps termed?' if 'deleted_user' in data['username'] else ''}\n"
            f"User ID: `{data['id']}`\n"
            f"Method of Scam: `{data['method']}`\n"
            f"Amount Scammed: `{data['amount']}`\n\n"
            f"{previous_aliases if previous_aliases else ''}"
        )

        return discord.Embed(title="Scammer Lookup", description=description, color=discord.Color.red())

    def generate_select_menu_options(self) -> list[discord.SelectOption]:
        options = [
            discord.SelectOption(
                label=f"{i+1}. {scammer['username']} {scammer['id']}",
                value=str(i)
            )
            for i in range(self.page * 10, min((self.page + 1) * 10, len(self.scammer_data)))
            if (scammer := self.scammer_data[i])
        ]
        return options

    def generate_content(self) -> str:
        return "\n".join(
            f"{i+1}. {scammer['username']} ({len(scammer.get('previous_aliases'))}) `{scammer['id']}`"
            for i in range(self.page * 10, min((self.page + 1) * 10, len(self.scammer_data)))
            if (scammer := self.scammer_data[i])
        )

    def generate_embed(self) -> discord.Embed:
        embed = discord.Embed(title="Scammer Lookup", description=self.generate_content(), color=discord.Color.red())
        embed.set_footer(text=f"Page {self.page+1}/{self.pages}")
        return embed

    async def previous_button(self, interaction: discord.Interaction) -> None:
        self.page = max(0, self.page - 1)
        await self.update_message(interaction)

    async def next_button(self, interaction: discord.Interaction) -> None:
        self.page = min(self.pages - 1, self.page + 1)
        await self.update_message(interaction)

    async def select_menu_callback(self, interaction: discord.Interaction) -> None:
        value = int(interaction.data['values'][0])
        scammer_data = self.scammer_data[value]
        await interaction.response.send_message(embed=self.generate_data_embed(scammer_data), ephemeral=True)

    async def update_message(self, interaction: discord.Interaction) -> None:
        self.children[2].options = self.generate_select_menu_options()
        await interaction.response.edit_message(embed=self.generate_embed(), view=self)

    async def on_timeout(self) -> None:
        for child in self.children:
            if isinstance(child, (Button, Select)):
                child.disabled = True
        await self.message.edit(view=self)
        await super().on_timeout()
