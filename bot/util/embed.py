import discord

def embed_generator(title: str="Error", description: str="An error occurred.", color: discord.colour = discord.Color.red()) -> discord.Embed:

    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="Made by notnomv6", icon_url="https://bots.noemt.dev/avatars/nom.png")
    
    return embed