import discord
from discord import Forbidden
from discord.ext import commands
from datetime import datetime

class Logs(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    self.log_channel = self.bot.get_channel(927265748445978694)

  #@commands.Cog.listener()
  #async def on_member_update(self, before, after):
    #if before.display_name != after.display_name:
      #embed = discord.Embed(title = "Nickname Change", colour = 0x33ff86, timestamp = datetime.utcnow())


      #embed.add_field(name = "Previous Name", value = before.display_name, inline = False)
      #embed.add_field(name = "Curent Name", value = after.display_name, inline = False)

      #await self.log_channel.send(embed = embed)

  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
    if not after.author.bot:
      if before.content != after.content:
        desc = "*Message From*: " + "**" + before.author.name + "#" + before.author.discriminator + "**\n" + "User ID: " + str(before.author.id)
        embed = discord.Embed(title = "Message Edit", description = desc ,colour = 0x33ff86, timestamp = datetime.utcnow())

        embed.set_thumbnail(url = before.author.avatar_url)

        embed.add_field(name = "Previous Message", value = before.content, inline = False)
        embed.add_field(name = "Current Message", value = after.content, inline = False)
          
        await self.log_channel.send(embed = embed)
      pass

  @commands.Cog.listener()
  async def on_message_delete(self, message):
    if not message.author.bot:
      desc = "*Message Deleted By*: " + "**" + message.author.name + "#" + message.author.discriminator + "**\n" + "User ID: " + str(message.author.id)
      embed = discord.Embed(title = "Deleted Message", description = desc ,colour = 0x33ff86, timestamp = datetime.utcnow())
      embed.set_thumbnail(url = message.author.avatar_url)

      embed.add_field(name = "Message", value = message.content, inline = False)
      await self.log_channel.send(embed = embed)

    pass


def setup(bot):
  bot.add_cog(Logs(bot))
    

  