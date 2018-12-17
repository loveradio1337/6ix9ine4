import discord
from discord.ext import commands
import random, asyncio, aiohttp, datetime

class premium():
    def __init__(self, bot):
        self.bot = bot

    def has_role_in_my_server(self):
        def wrapper(self, ctx):
            server = self.bot.get_guild(455305359645736971)
            role = discord.utils.get(server.roles, name="premium")
            user = discord.utils.get(server.members, id=ctx.author.id)
            if not user or not role: return False
            return role in user.roles
        return commands.check(wrapper)

def setup(bot):
    bot.add_cog(premium(bot))