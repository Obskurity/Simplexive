import discord
from discord.ext import commands 
import os
import pymongo
from pymongo import MongoClient


#bot = discord.Client()
bot = commands.Bot(command_prefix = "!")
bot.remove_command("help")

@bot.event
async def on_ready():
  client = MongoClient(str(os.environ['HOSTNAME'])
  db = client.db_name
  print("Initiallized Database.......")
  print('Running as {0.user}'.format(bot))
  await bot.change_presence(activity = discord.Game(name = "!help for more about me."))
  


@bot.event 
async def on_message(message):
  if message.author == bot.user:
    return

  await bot.process_commands(message)

@bot.command()
async def load(ctx, extension):
  bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
  if(filename.endswith('.py')):
    bot.load_extension(f'cogs.{filename[:-3]}')




bot.run(os.environ['TOKEN'])

