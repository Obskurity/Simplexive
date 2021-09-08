import discord
from discord.ext import commands

class Info(commands.Cog, description = "Cog responsible for displayin information about the server or the user."):
  """
  Module responsible for displayin information about the server or the user.
  """
  def __init__(self, bot):
    self.bot = bot

  @commands.command(description = "Displays information about a user.")  
  async def userinfo(self, ctx):
    user = ctx.author
    embed = discord.Embed(title = "USER INFO", description = f"Here is the information that I have found on {user}", colour = 0x33ff86)#user.colour)
    embed.set_thumbnail(url = user.avatar_url)
    embed.add_field(name = "Name", value = user.name, inline = False)
    embed.add_field(name = "ID", value = user.id, inline = True)
    embed.add_field(name = "Status", value = user.status, inline = True)
    await ctx.send(embed = embed)

  @commands.command(description = "Displays information about the current server.") 
  async def serverinfo(self, ctx):
    discServer = ctx.guild

    embed = discord.Embed(title = f"{discServer.name}", description = f"{discServer.description}", colour = 0x33ff86)
    embed.set_thumbnail(url = discServer.icon_url)
    embed.add_field(name = "Server Owner", value = discServer.owner, inline = False)
    embed.add_field(name = "Server ID", value = discServer.id, inline = True)
    embed.add_field(name = "Region", value = discServer.region, inline = True)
    embed.add_field(name = "Member Count", value = discServer.member_count, inline = True)
    embed.add_field(name = "Server Creation Date", value = discServer.created_at, inline = True)
    embed.add_field(name = "Emotes", value = discServer.emojis, inline = False)
    await ctx.send(embed = embed)


def setup(bot):
  bot.add_cog(Info(bot))