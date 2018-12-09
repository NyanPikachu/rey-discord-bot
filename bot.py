import discord
from discord.ext import commands
import os
import sys
from motor import motor_asyncio
import requests
import json
from ext import utils

dbclient = motor_asyncio.AsyncIOMotorClient('mongodb://brawlstats:' + os.environ.get("DBPASS") + '@ds255329.mlab.com:55329/hellobitgame')
db = dbclient.hellobitgame

async def get_pre(bot, message):
    try:
        result = await db.settings.find_one({'_id': str(message.guild.id)})
    except AttributeError:
        return "!"
    if not result or not result.get('prefix'):
        return "!"
    return result['prefix']


bot = commands.Bot(command_prefix=get_pre, description="A simple bot made by Parzival#4148 for BrawlStarRey's discord server!", owner_id=279974491071709194)
bot.load_extension("cogs.brawlstars")

async def save_prefix(prefix, guildID):
    await db.settings.update_one({'_id': guildID}, {'$set': {'_id': guildID, 'prefix': prefix}}, upsert=True)

@bot.event
async def on_ready():
    print("Bot is online!")
    await bot.change_presence(activity=discord.Activity(name=f'Made by Parzival#4148, powered by brawlapi.cf | !help', type=discord.ActivityType.playing))
    
@bot.command(hidden=True)
async def ping(ctx):
    '''Pong! Get the bot's response time'''
    em = discord.Embed(color=discord.Color.gold())
    em.title = "Pong!"
    em.description = f'{bot.latency * 1000:.0f} ms'
    await ctx.send(embed=em)
    
@bot.command()
@commands.has_permissions(manage_messages=True)
async def prefix(ctx, prefix=None):
    """Change Prefix of the server"""
    guildID = str(ctx.guild.id)
    if not prefix:
        return await ctx.send('Please provide a prefix for this command to work')
    try:
        await save_prefix(prefix, guildID)
        await ctx.send(f'Prefix `{prefix}` successfully saved (re-run this command to replace it)')
    except Exception as e:
        await ctx.send(f'Something went wrong\nError Log: `str({e})`')
    
@bot.command()
async def bug(ctx):
    """Report a bug!"""
    await ctx.send('If you find any bugs please make sure to report them to me! username: Parzival#4148')

bot.run(os.environ.get("TOKEN"))