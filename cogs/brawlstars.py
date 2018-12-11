import discord
from discord.ext import commands
import os
import sys
from motor import motor_asyncio
import requests
import json
from ext import utils

class BrawlStars:
    '''Brawl Stars commands to get your brawling stats on demand!'''
    def __init__(self, bot):
        self.bot = bot
        self.dbclient = motor_asyncio.AsyncIOMotorClient('mongodb://nyanpikachu:' + os.environ.get('DBPASS') + '@ds115740.mlab.com:15740/brawlstats')
        self.db = self.dbclient.brawlstats
        self.headers = {
            "Authorization": os.environ.get("BSTOKEN")
            }
            
    def get_info(self, tag):
        r = requests.get(f'https://brawlapi.cf/api/players/{tag}', headers=self.headers)
        req = r.json()

    async def save_tag(self, tag, userID):
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
    async def bsprofile(self, ctx, tag: str=None):
        '''Gets your Brawl Stars Profile using a Tag'''
        authorID = str(ctx.author.id)
        if not tag:
            if await self.get_tag(authorID) == 'None':
                await ctx.send(f'Please provide a tag or save your tag using `{ctx.prefix}bssave <tag>`')
            tag = await self.get_tag(authorID)
        data = self.get_info(tag)
        em = discord.Embed(color=utils.random_color())
        em.title = f'{data["name"]}\'s info'
        em.description = data["tag"]
        em.add_field(name="Trophies", value=data["trophies"])
        em.add_field(name="Highest Trophies", value=data["highestTrophies"])
        em.add_field(name="3v3 Victories", value=data["victories"])
        em.add_field(name="Showdown Victories", value=data["soloShowdownVictories"])
        em.add_field(name="Duo Showdown victories", value=data["duoShowdownVictories"])
        em.add_field(name="Level", value=data["expLevel"])
        em.add_field(name="Experience", value=data["expFmt"])
        em.add_field(name="Total Experience", value=data["totalExp"])
        em.add_field(name="Brawlers", value=data["brawlersUnlocked"])
        em.add_field(name="Best time as The Boss", value=data["bestTimeAsBoss"])
        em.add_field(name="Best Robo Rumble Time", value=data["bestRoboRumbleTime"])
        em.add_field(name="Club", value=data["club"]["name"])
        
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(BrawlStars(bot))