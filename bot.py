import discord, datetime
from discord.ext import commands
import os, asyncio,aiohttp
from motor.motor_asyncio import AsyncIOMotorClient

async def getprefix(bot, message):
    if isinstance(message.channel, discord.DMChannel):
        return commands.when_mentioned_or(">")(bot, message)
    try:
        x = await bot.db.prefixes.find_one({ "id": message.guild.id })
        if not x:
            return commands.when_mentioned_or(">")(bot, message)
        prefix = x['prefix']
        return commands.when_mentioned_or(prefix)(bot, message)
    except:
        return commands.when_mentioned_or(">")(bot, message)

bot = commands.Bot(command_prefix=getprefix)
bot.session = aiohttp.ClientSession(loop=bot.loop)                       
bot.remove_command('help')

bot.load_extension("cogs.fun")
bot.load_extension("cogs.images")
bot.load_extension("cogs.info")
bot.load_extension("cogs.utility")
bot.load_extension("cogs.economy")
bot.load_extension("cogs.mod")
bot.load_extension("cogs.owner")
bot.load_extension("cogs.giveaway")
bot.load_extension("cogs.source")
bot.load_extension("cogs.tags")

@bot.event
async def on_command_error(message, error):
        print(error)
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(color=0xff2d32, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Error", value=f"{error}")
            await discord.abc.Messageable.send(message.channel, embed=embed)
        if isinstance(error, commands.NotOwner):
            em = discord.Embed(color=0xff2d322, timestamp=datetime.datetime.utcnow())
            em.add_field(name="Error", value="Your not my daddy!")
            await message.channel.send(embed=em)

@bot.event
async def on_ready():
    print('Bot is online, and ready to ROLL!')
    while True:
        await bot.change_presence(activity=discord.Game(name=f">help"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name=f"with ma god Vilgot"))
        await asyncio.sleep(10)
@bot.event  
async def on_guild_join(guild):
    lol = bot.get_channel(461050385583570954)
    em = discord.Embed(color=discord.Color(value=0x11f95e))
    em.title = "I have joined new server!"
    em.description = f"Server: {guild}"
    em.add_field(name="Members", value=len(guild.members))
    em.add_field(name="Owner", value=guild.owner)
    em.set_thumbnail(url=guild.icon_url)
    em.set_footer(text=f"ID: {guild.id}")
    await lol.send(embed=em)
    try:
        await guild.channels[0].send(f"Hello! Thanks for adding meh!")
    except discord.Forbidden:
        pass

@bot.event
async def on_guild_remove(guild):
    lol = bot.get_channel(461050385583570954)
    em = discord.Embed(color=discord.Color(value=0xf44242))
    em.title = "One server less"
    em.description = f"Server: {guild}"
    em.set_footer(text=f"ID: {guild.id}")
    em.set_thumbnail(url=guild.icon_url)
    await lol.send(embed=em)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)
    
@bot.command()
async def help(ctx, cmd: str = None):
    """This thing"""#
    if cmd is None:
        embed = discord.Embed(title="My commands", color=0x9b9dff)
        embed.add_field(name="Info", value="`help`, `stats`, `invite`", inline=False)
        embed.add_field(name="Fun", value="`roast`, `alert`, `lmgtfy`,  `face`, `lenny`, `tableflip`, `meme`, `alia`, `anthem`, `bongocat`, `tweet`, `rip`, `achievement`", inline=False)
        embed.add_field(name="Economy", value="`openaccount`, `earn`, `bal`, `daily`", inline=False)
        embed.add_field(name="Moderation", value="`welcome`, `leave`, `welcomeimage`, `modlog`, `lockdown`, `autorole`, `kick`, `ban`, `purge`, `warn`, `mute`, `unmute`", inline=False)
        embed.add_field(name="Giveaway", value="`start`", inline=False)
        embed.add_field(name="Utility", value="`8ball`, `serverinfo`, `userinfo`, `ping`, `prefix`, `avatar`", inline=False)
        await ctx.send(embed=embed)
    if cmd:
        x = bot.get_command(cmd)
        y = await bot.db.prefixes.find_one({ "id": ctx.guild.id })
        if not y:
            return await ctx.send(f"```fix\n> {cmd} >\n= {x.help}\nUsage: >{x.signature}```")
        await ctx.send(f"```fix\n> {cmd} >\n = {x.help}\nUsage: {y['prefix']}{x.signature}```")
    elif command is None:
        await ctx.send("That command doesnt exist!")

@bot.command()
@commands.is_owner()
async def load(ctx, cog: str):
    """Loads an extension."""
    try:
        bot.load_extension(f"cogs.{cog}")
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send(f"Loaded cogs.{cog}")


@bot.command()
@commands.is_owner()
async def unload(ctx, cog: str):
    bot.unload_extension(f"cogs.{cog}")
    await ctx.send(f"Unloaded cogs.{cog}")

@bot.command()
async def cat(ctx):
    res = await bot.session.get("https://catapi.glitch.me/")
    data = await res.json()
    embed = discord.Embed(color=0x36393E)
    embed.set_image(url = data['url'])
    await ctx.send("**Heres your random cat**",embed=embed)
    await session.close()
                       
@bot.command()
async def reload(ctx, cog: str):
    x = await ctx.send(f"Reloading {cog}!")
    bot.unload_extension(f"cogs.{cog}")
    bot.load_extension(f"cogs.{cog}")
    await x.edit(content=f"Realoded {cog}!")

def has_role_in_my_server(name):
    def wrapper(ctx):
        server = bot.get_guild(455305359645736971)
        role = discord.utils.get(server.roles, name=name)
        user = discord.utils.get(server.members, id=ctx.author.id)
        if not user or not role: return False
        return role in user.roles
    return commands.check(wrapper)

@bot.command()                       
@has_role_in_my_server("premium")
async def repeat(ctx, times: int,*, content : str):
    for i in range(times):
        await ctx.send(content)

#@bot.event
#async def on_raw_reaction_add(payload):
    #vilgot_id = 338600456383234058
    #channel = bot.get_channel(payload.channel_id)
    #if channel.id != 457623659369070642:
        #return
    #msg = await channel.get_message(payload.message_id)
    #reactions = list(filter(lambda x: x.emoji == "✅", msg.reactions))
    #print(reactions)
    #if reactions[0].count > 3:
        #embed=discord.Embed(title="Suggestion got over 3 votes!", description=payload.message.content)
        #await vilgot_id.send(embed=embed)
 

                       
db = AsyncIOMotorClient(os.environ.get("MONGODB"))
bot.db = db.pepe_my_bot

if not os.environ.get('TOKEN'):
    print("no token found")
bot.run(os.environ.get('TOKEN').strip('"'))