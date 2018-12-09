import discord
from discord.ext import commands
import os
import sys
from motor import motor_asyncio
import requests
import json
from ext import utils

class BrawlStats:
    '''Brawl Stars commands to get your brawling stats on demand!'''
    def __init__(self, bot):
        self.bot = bot
        self.token = (os.environ.get('BSTOKEN'))
        self.dbclient = motor_asyncio.AsyncIOMotorClient('mongodb://brawlstats:' + os.environ.get('DBPASS') + '@ds115740.mlab.com:15740/brawlstats')
        self.db = self.dbclient.brawlstats

    async def save_tag(tag, userID):
    	await db.brawlstats.update_one({'_id': userID}, {'$set': {'_id': userID, 'tag': tag}}, upsert=True)

    async def get_tag(self, authorID):
        result = await self.db.clashroyale.find_one({'_id': authorID})
        if not result:
            return 'None'
        return result['tag']

    def emoji(self, emoji):
        with open('data/emojis.json') as f:
            emojis = json.load(f)
            e = emojis[emoji]
        return self.bot.get_emoji(e)

    @commands.command()
    async def bssave(self, ctx, tag=None):
        """Save your Brawl Stars tag"""
        authorID = str(ctx.author.id)
        if not tag:
            return await ctx.send(f'Please provide a tag `Usage: crsave tag`')
        tag = tag.strip('#').replace('O', '0')
        await self.save_tag(tag, authorID)
        await ctx.send(f'Your tag `#{tag}` has been successfully saved')

    @commands.command()
    async def bsprofile(self, ctx, tag: str=None, user: discord.Member):
        '''Gets your Brawl Stars Profile using a Tag'''
        authorID = str(ctx.author.id)
        if not tag:
            if await self.get_tag(authorID) == 'None':
                await ctx.send(f'Please provide a tag or save your tag using `{ctx.prefix}crsave <tag>`')
            tag = await self.get_tag(authorID)

def setup(bot):
    bot.add_cog(Clash_Royale(bot))