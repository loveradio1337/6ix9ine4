import discord
from discord.ext import commands
import random, asyncio, aiohttp, datetime

class tags():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tag(self, ctx, sort=None, name=None,*, description=None):
        if sort == None:
            await ctx.send("Select a tag")
        if sort == "create":
            await self.bot.db.tags.update_one({"name": name}, {"$set": {"description": description} }, upsert=True )
            await ctx.message.add_reaction('✅')
        else:
            x = await self.bot.db.tags.find_one({"name": sort })
            await ctx.send(x['description'])
            
def setup(bot):
    bot.add_cog(tags(bot))
