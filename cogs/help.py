import discord
from discord.ext import commands


class Help(commands.Cog, description = 'Cog responsible for helping out users.'):
  """
  Sends the help command.
  """
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def help(self, ctx, *input):
    #credit: https://gist.github.com/nonchris/1c7060a14a9d94e7929aa2ef14c41bc2
    if not input:
      # starting to build embed
      helpCommandEmbed = discord.Embed(title='Command Categories', description = f'Use `!help [category]` to see the commands under that category.', colour = 0x33ff86)

      # iterating through cogs, gathering descriptions
      cogs_desc = ''
      for cog in self.bot.cogs:
        cogs_desc += f'__{cog}__ {self.bot.cogs[cog].__doc__}\n'

      # adding 'list' of cogs to embed
      helpCommandEmbed.add_field(name = 'Categories', value = cogs_desc, inline = False)

      # integrating trough uncategorized commands
      commands_desc = ''
      for command in self.bot.walk_commands():
        # if cog not in a cog
        # listing command if cog name is None and command isn't hidden
        if not command.cog_name and not command.hidden:
          commands_desc += f'{command.name} - {command.help}\n'

    # block called when one cog-name is given
    # trying to find matching cog and it's commands
    elif len(input) == 1:
      # iterating trough cogs
      for cog in self.bot.cogs:
        # check if cog is the matching one
        if cog.lower() == input[0].lower():
          # making title - getting description from doc-string below class
          helpCommandEmbed = discord.Embed(title = f'{cog} - Commands', description = self.bot.cogs[cog].__doc__, colour = 0x33ff86)

          # getting commands from cog
          for command in self.bot.get_cog(cog).get_commands():
            # if cog is not hidden
            if not command.hidden:
              helpCommandEmbed.add_field(name = f"**__!{command.name}__**", value = command.description, inline = True)
          # found cog - breaking loop
          break
        # if input not found
      else:
        helpCommandEmbed = discord.Embed(title = f"{input[0]} is nota  cateogry.", description = "Please request a category instead.", colour = 0x33ff86)

    # when someone passed in more than one category(i.e, argument)
    elif len(input) > 1:
      helpCommandEmbed = discord.Embed(description = "Please request only one category at a time :smiley:", colour = 0x33ff86)

    else:
      return

    await ctx.send(embed = helpCommandEmbed)

def setup(bot):
  bot.add_cog(Help(bot))

