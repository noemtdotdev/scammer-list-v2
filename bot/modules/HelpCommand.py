import discord
from discord.ext import commands
from bot.bot import Bot

class HelpCommand(commands.Cog):
    def __init__(self, bot):

        self.bot:Bot = bot

    @commands.slash_command(
        name="help",
        description="Shows a list of commands.",
        integration_types={discord.IntegrationType.user_install, discord.IntegrationType.guild_install}
    )
    async def help(self, ctx: discord.ApplicationContext):

        all_commands = ""
        for cog in self.bot.cogs:
            for command in self.bot.get_cog(cog).walk_commands():

                if isinstance(commands, discord.SlashCommandGroup):
                    continue


                if not isinstance(command, discord.SlashCommand):
                    continue
                

                string = f"</{command.qualified_name}:{command.qualified_id}> "
                for option in command.options:
                    string += f"`[{option.name}]` " if option.required else f"`<{option.name}>` "

                string += "\n"
                all_commands += string


        embed = discord.Embed(
            title="Help",
            color=discord.Color.red(),
            description="[..] = Required, <..> = Optional\n\n"+all_commands
        )
    
        await ctx.respond(embed=embed)

    @commands.slash_command(
        name="info",
        description="Shows information about the bot.",
        integration_types={discord.IntegrationType.user_install, discord.IntegrationType.guild_install}
    )
    async def info(self, ctx:discord.ApplicationContext):

        view = discord.ui.View()
        support_button = discord.ui.Button(row=0, label="Support Server", url="https://discord.gg/949Ekcpf")
        website_button = discord.ui.Button(row=0, label="Source Code", url="https://github.com/noemtdotdev/scammer-list-v2")
        privacy_policy = discord.ui.Button(row=1, label="Privacy Policy", url="https://noemt.dev/privacy")

        view.add_item(support_button)
        view.add_item(website_button)
        view.add_item(privacy_policy)

        embed = discord.Embed(
            title="Info",
            color=discord.Color.red(),
            description="A bot to help you not to deal with scammers."
        )
        embed.set_author(name="@notnomv6", icon_url="https://bots.noemt.dev/avatars/nom.png", url="https://github.com/noemtdotdev")
        embed.set_image(url=self.bot.user.avatar.url)

        embed.add_field(
            name="Programming Language",
            value="`🐍` Python (py-cord 2.6.0)",
            inline=False
        )

        embed.add_field(
            name="Hosting",
            value="`🌐` Hetzner",
        )

        embed.add_field(
            name="`🧑‍💻` Developer",
            value="`@notnomv6`",
        )

        collection = self.bot.db['staff']
        staff = collection.find({})
        if staff:
            content = ""
            for staff_member in staff:
                content += f"• <@{staff_member['id']}> - `{staff_member['username']}`\n"

            embed.add_field(
                name="`🧑` Staff",
                value=content,
                inline=False
            )

        await ctx.respond(embed=embed, view=view)



def setup(bot:Bot):
    bot.add_cog(HelpCommand(bot))