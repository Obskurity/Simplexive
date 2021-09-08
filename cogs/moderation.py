import discord
from discord.ext import commands

class Moderation(commands.Cog, description = "Responsible for the moderation of servers."):
  """
  Module Responsible for the moderation of servers.
  """
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(description = "Kicks members from the server.\n`!kick [member] [reason]`")
  @commands.has_permissions(kick_members = True)  
  async def kick(self, ctx, member: discord.Member = None, *, reason = None):
    if member == None:
      channelEmbed = discord.Embed(title = "**Kick**", description = "Kicks a user from the server.\nTry `!kick [member] [reason]`\n", colour = 0x33ff86)
      channelEmbed.add_field(name = 'Example', value = "`!kick @Bobby#0000`\n`!kick @Joe#1111 spamming`")
      await ctx.send(embed = channelEmbed) 
      return

    if reason != None: 
      embed = discord.Embed(description = f"You were kicked from **{ctx.guild.name}**.\nReason: {reason}.", colour = 0x33ff86)
      await member.send(embed = embed)
      channelEmbed = discord.Embed(description = f"{member} was kicked for {reason}.", colour = 0x33ff86)
    else:
      embed = discord.Embed(description = f"You were kicked from **{ctx.guild.name}**.\nReason not specified.", colour = 0x33ff86)
      await member.send(embed = embed)
      channelEmbed = discord.Embed(description = f"{member} was kicked.", colour = 0x33ff86)
    await ctx.send(embed = channelEmbed) 
    await member.kick(reason = reason)

  @commands.command(description = "Bans members from the server.\n`!ban [member] [reason]`")
  @commands.has_permissions(ban_members = True)
  async def ban(self, ctx, member: discord.Member = None, reason = None):
    if member == None:
      channelEmbed = discord.Embed(title = "**Ban**", description = "Bans a user from the server.\nTry `!ban [member] [reason]`\n", colour = 0x33ff86)
      channelEmbed.add_field(name = 'Example', value = "`!ban @Bobby#0000`\n`!ban @Joe#1111 violating rules`")
      await ctx.send(embed = channelEmbed) 
      return
      
    if reason != None:  
      embed = discord.Embed(description = f"You were banned from **{ctx.guild.name}**.\nReason: {reason}.", colour = 0x33ff86)
      await member.send(embed = embed)
      channelEmbed = discord.Embed(description = f"{member} was banned for {reason}.", colour = 0x33ff86)    
    else: 
      embed = discord.Embed(description = f"You were banned from **{ctx.guild.name}**.\nReason not specified.", colour = 0x33ff86)
      await member.send(embed = embed)
      channelEmbed = discord.Embed(description = f"{member} was banned.", colour = 0x33ff86)  
    await ctx.send(embed = channelEmbed) 
    await member.ban(reason = reason)

  @commands.command(description = "Mutes a member from  the server.\n`!mute [member] [reason]`")
  @commands.has_permissions(manage_messages = True)
  async def mute(self, ctx, member: discord.Member = None,  *, reason = None):
    if member == None:
      channelEmbed = discord.Embed(title = "**Mute**", description = "Prevents users from typing and speaking.\nTry `!mute [member] [reason]`\n", colour = 0x33ff86)
      channelEmbed.add_field(name = 'Example', value = "`!mute @Bobby#0000`\n`!mute @Joe#1111 posting rickrolls`")
      await ctx.send(embed = channelEmbed) 
      return

    if(member.guild_permissions.administrator):
      channelEmbed = discord.Embed(description = "Administrators/Moderators cannot be muted. :x:", colour = 0x33ff86)
      await ctx.send(embed = channelEmbed)
      return
    else:
      discServer = ctx.guild
      muteRole = discord.utils.get(discServer.roles, name = "Muted")
      if not muteRole:
        muteRole = await discServer.create_role(name = "Muted")
        for channel in discServer.channels:
          await channel.set_permissions(muteRole, speak = False, send_messages = False, read_message_history = True, read_messages = True)
      
      # checks if person is already muted
      if muteRole not in member.roles:
        await member.add_roles(muteRole, reason = reason)
      else:
        channelEmbed = discord.Embed(description ="User is already muted.", colour = 0x33ff86)
        await ctx.send(embed = channelEmbed)
        return
        
      embed = None
      embedDM = None

      if (reason != None):
        embed = discord.Embed(description = f"{member} was muted for **{reason}**.", colour = 0x33ff86)
        embedDM = discord.Embed(description = f"You were muted in {discServer.name} for **{reason}**.",colour = 0x33ff86)
      else:
        embed = discord.Embed(description = f"{member} was muted.", colour = 0x33ff86)
        embedDM = discord.Embed(description = f"You were muted in {discServer.name}.",colour = 0x33ff86)

      await ctx.send(embed = embed)
      await member.send(embed = embedDM)


  @commands.command(description = "Unmutes a member from the server.\n`!unmute [member]`")
  @commands.has_permissions(manage_messages = True)
  async def unmute(self, ctx, member: discord.Member = None):
    if member == None:
      channelEmbed = discord.Embed(title = "**Unmute**", description = "Try `!mute [member]`\n", colour = 0x33ff86)
      channelEmbed.add_field(name = 'Example', value = "`!unmute @Bobby#0000`")
      await ctx.send(embed = channelEmbed) 
      return
     
    discServer = ctx.guild
    muteRole = discord.utils.get(discServer.roles, name = "Muted")
    if muteRole in member.roles:
      await member.remove_roles(muteRole)
      embed = discord.Embed(description = f"{member} has been unmuted.", colour = 0x33ff86)
      embedDM = discord.Embed(description = f"You were unmuted in {discServer.name}.",colour = 0x33ff86)
      await ctx.send(embed = embed)
      await member.send(embed = embedDM)
    else:
      embed = discord.Embed(description = f"{member} is not currently muted.", colour = 0x33ff86)
      await ctx.send(embed = embed)

  @commands.command(description = "Clears all messages in a text channel.")
  @commands.has_permissions(administrator = True)
  async def clearall(self, ctx):
    await ctx.channel.purge()

  @commands.command(description = "Clears  a certain amount of messages in a text channel.\n`!clear [message amount as a number]`")
  @commands.has_permissions(administrator = True)
  async def clear(self, ctx, amount: int = 0):
    if amount > 0:
      await ctx.channel.purge(limit = amount)
    else:
      channelEmbed = discord.Embed(title = "**Clear**", description = "Try `!clear [message amount(must be > 0)]`\n", colour = 0x33ff86)
      channelEmbed.add_field(name = 'Example', value = "`!clear 1000`")
      await ctx.send(embed = channelEmbed) 

  @commands.command(description = "Locks the current text channel.")
  @commands.has_permissions(manage_channels = True)
  async def lock(self, ctx):
    discServer = ctx.guild
    embed = discord.Embed(description = "Channel is now locked.", colour = 0x33ff86)
    perm = ctx.channel.overwrites_for(discServer.default_role)
    perm.send_messages = False
    await ctx.channel.set_permissions(discServer.default_role, overwrite = perm)      
    await ctx.send(embed = embed)

  @commands.command(description = "Unlocks the current text channel.")
  @commands.has_permissions(manage_channels = True)
  async def unlock(self, ctx):
    discServer = ctx.guild
    embed = discord.Embed(description = "Channel is now unlocked.", colour = 0x33ff86)
    perm = ctx.channel.overwrites_for(discServer.default_role)
    perm.send_messages = True
    await ctx.channel.set_permissions(discServer.default_role, overwrite = perm)      
    await ctx.send(embed = embed)
      


  #@commands.Cog.listener()
  #async def on_message(self, message):
    #if any(word in message.content for word in db[f"{ctx.guild.name}"]):
      #await message.delete()
      #await message.author.send("You may not ping that user.")


  #@commands.command(name = "blockmention", description = "prevents a user from being @'ed")
 #@commands.has_permissions(administrator = True)
  #async def blockmention(self, ctx, member: discord.Member):
    #db[f"{ctx.guild.name}"] = f"{member.mention}"
    #await ctx.send(f"{member.name} was added to the blockmention list")



def setup(bot):
  bot.add_cog(Moderation(bot))
  
