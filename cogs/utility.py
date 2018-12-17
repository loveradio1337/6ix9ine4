import discord
from discord.ext import commands
import random, time

class utility():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball")
    async def eight_ball(self, ctx,*, question):
        """Ask me a question"""
        answers = ["Yes", "No", "Ask later", "Such a silly question", "of course"]
        answer = random.choice(answers)
        embed=discord.Embed(description=f"Question: **{question}**\n\nAnswer: **{answer}**", color=0x9b9dff)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        """See some information about the server"""
        guild = ctx.guild
        time = str(guild.created_at.strftime("%b %m, %Y, %A, %I:%M %p"))
        embed=discord.Embed(description=f"**{guild.name}**\nOwner: **{guild.owner.mention}**\nMembers: **{len(guild.members)}**\nRoles: **{len(guild.roles)}**\nVerification level: **{guild.verification_level}**\nCreated at: **{'%s' % time}**", color=0x06ff06)
        embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)

    #@commands.command()
    #async def roles(self, ctx):
        #await ctx.send(f"```fix\n= There is {} in this server.\n\n- {return [x.name for x in ctx.guild.roles]}```")
                            
    @commands.command()
    async def userinfo(self, ctx, user: discord.Member):
        """See some information about a user"""
        join_time = str(ctx.author.joined_at.strftime("%b %m, %Y, %A, %I:%M %p"))
        embed=discord.Embed(description=f"{user.mention}\nId: **{user.id}**\nRoles: **{len(user.roles)}**\nStatus: **{user.status}**\nJoined at: **{'%s' % join_time}**", color=user.color)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping_command(self, ctx):
        """:ping_pong: Pong! My latency"""
        t1 = time.perf_counter()
        message = await ctx.send("checking ping...")
        t2 = time.perf_counter()
        ping = round((t2-t1)*1000)
        await message.edit(content=f":ping_pong: Pong! `{ping}`ms")                                                     
    
    @commands.command()
    async def add(self, ctx, num1:int, num2:int):
        await ctx.send(int(num1) + int(num2))

    @commands.command()
    async def subtract(self, ctx, num1:int, num2:int):
        await ctx.send(int(num1) - int(num2))

    @commands.command()
    async def multiply(self, ctx, num1:int, num2:int):
        await ctx.send(int(num1) * int(num2))

    @commands.command()
    async def divide(self, ctx, num1:int, num2:int):
        await ctx.send(int(num1) / int(num2))                          
                            
def setup(bot):
    bot.add_cog(utility(bot))
