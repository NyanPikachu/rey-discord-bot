import discord
from discord.ext import commands
import os
import sys
from motor import motor_asyncio
import requests
import json
from ext import utils
from ext.paginator import Paginator

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
        return req

    def get_all_events(self):
        r = requests.get(f'https://brawlapi.cf/api/events', headers=self.headers)
        req = r.json()
        return req

    def get_events(self, type):
        r = requests.get(f'https://brawlapi.cf/api/events', headers=self.headers)
        req = r.json()
        return req

    async def save_tag(self, tag, userID):
        await self.db.brawlstats.update_one({'_id': userID}, {'$set': {'_id': userID, 'tag': tag}}, upsert=True)

    async def get_tag(self, authorID):
        result = await self.db.brawlstats.find_one({'_id': authorID})
        if not result:
            return 'None'
        return result['tag']

    def emoji(self, emoji):
        with open('data/emojis.json') as f:
            emojis = json.load(f)
            e = emojis[emoji]
        return self.bot.get_emoji(e)

    @commands.command()
    async def bsevents(self, ctx):
        data = self.get_all_events()

        ticketedEvent = True

        try:
            data["current"][4]["gameMode"]
        except:
            ticketedEvent = False

        embeds = []

        em = discord.Embed(color=utils.random_color())
        em.title = data["current"][0]["slotName"]
        em.set_image(url=data["current"][0]["mapImageUrl"])
        em.add_field(name='Event Name', value=data["current"][0]["gameMode"])
        em.add_field(name='Slot Number', value=data["current"][0]["slot"])
        em.add_field(name='Map', value=data["current"][0]["mapName"])
        em.add_field(name='Free Keys', value=data["current"][0]["freeKeys"])
        embeds.append(em)

        em = discord.Embed(color=utils.random_color())
        em.set_image(url=data["current"][1]["mapImageUrl"])
        em.title = data["current"][1]["slotName"]
        em.add_field(name='Event Name', value=data["current"][1]["gameMode"])
        em.add_field(name='Slot Number', value=data["current"][1]["slot"])
        em.add_field(name='Map', value=data["current"][1]["mapName"])
        em.add_field(name='Free Keys', value=data["current"][1]["freeKeys"])
        embeds.append(em)

        em = discord.Embed(color=utils.random_color())
        em.set_image(url=data["current"][2]["mapImageUrl"])
        em.title = data["current"][2]["slotName"]
        em.add_field(name='Event Name', value=data["current"][2]["gameMode"])
        em.add_field(name='Slot Number', value=data["current"][2]["slot"])
        em.add_field(name='Map', value=data["current"][2]["mapName"])
        em.add_field(name='Free Keys', value=data["current"][2]["freeKeys"])
        embeds.append(em)

        em = discord.Embed(color=utils.random_color())
        em.set_image(url=data["current"][3]["mapImageUrl"])
        em.title = data["current"][3]["slotName"]
        em.add_field(name='Event Name', value=data["current"][3]["gameMode"])
        em.add_field(name='Slot Number', value=data["current"][3]["slot"])
        em.add_field(name='Map', value=data["current"][3]["mapName"])
        em.add_field(name='Free Keys', value=data["current"][3]["freeKeys"])
        embeds.append(em)

        if ticketedEvent:
            em = discord.Embed(color=utils.random_color())
            em.set_image(url=data["current"][4]["mapImageUrl"])
            em.title = data["current"][4]["slotName"]
            em.add_field(name='Event Name', value=data["current"][4]["gameMode"])
            em.add_field(name='Slot Number', value=data["current"][4]["slot"])
            em.add_field(name='Map', value=data["current"][4]["mapName"])
            em.add_field(name="Modifier", value=data["current"][4]["modifierName"])
            em.add_field(name='Free Keys', value=data["current"][4]["freeKeys"])
            embeds.append(em)

        p_session = Paginator(ctx, footer=f'Made by Parzival#4148', pages=embeds)
        await p_session.run()
        
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
                return await ctx.send(f'Please provide a tag or save your tag using `{ctx.prefix}bssave <tag>`')
            tag = await self.get_tag(authorID)
        data = self.get_info(tag)
        
        hasClub = True
        
        try:
            data["club"]["name"]
        except:
            hasClub = False 
            
        embeds = []
        
        em = discord.Embed(color=utils.random_color())
        em.set_thumbnail(url=data["avatarUrl"])
        em.title = data["name"]
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
        embeds.append(em)
        
        if hasClub:
            em = discord.Embed(color=utils.random_color())
            em.set_thumbnail(url=data["club"]["badgeUrl"])
            em.add_field(name="Club", value=data["club"]["name"])
            em.add_field(name="Club Tag", value=data["bestRoboRumbleTime"])
            em.add_field(name="Role", value=data["club"]["role"])
            em.add_field(name="Members", value=data["club"]["members"])
            em.add_field(name="Trophies", value=data["club"]["trophies"])
            em.add_field(name="Required Trophies", value=data["club"]["requiredTrophies"])
            em.add_field(name="Online Members", value=f'There are ' + str(data["club"]["onlineMembers"]) + ' member(s) online!')
            embeds.append(em)
        
        p_session = Paginator(ctx, footer=f'Made by Parzival#4148', pages=embeds)
        await p_session.run()
        
    @commands.command()
    async def bsclub(self, ctx, tag: str=None):
        '''Gets your Brawl Stars Club info using a Tag'''
        authorID = str(ctx.author.id)
        if not tag:
            if await self.get_tag(authorID) == 'None':
                return await ctx.send(f'Please provide a tag or save your tag using `{ctx.prefix}bssave <tag>`')
            tag = await self.get_tag(authorID)
        data = self.get_info(tag)
        
        hasClub = True
        
        try:
            data["club"]["name"]
        except:
            hasClub = False
        
        if hasClub:
            em = discord.Embed(color=utils.random_color())
            em.set_thumbnail(url=data["club"]["badgeUrl"])
            em.add_field(name="Club", value=data["club"]["name"])
            em.add_field(name="Club Tag", value=data["bestRoboRumbleTime"])
            em.add_field(name="Role", value=data["club"]["role"])
            em.add_field(name="Members", value=data["club"]["members"])
            em.add_field(name="Trophies", value=data["club"]["trophies"])
            em.add_field(name="Required Trophies", value=data["club"]["requiredTrophies"])
            em.add_field(name="Online Members", value=f'There are ' + str(data["club"]["onlineMembers"]) + ' member(s) online!')
            await ctx.send(embed=em)
        else:
            await ctx.send("Oops, looks like you are not in a club yet! Consider joining one. They are great for finding a Team")
        
def setup(bot):
    bot.add_cog(BrawlStars(bot))