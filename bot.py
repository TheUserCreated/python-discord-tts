import asyncio
from collections import deque
from tempfile import TemporaryFile
import asyncpg
import ast
import discord
from discord.ext import commands
from gtts import gTTS

TOKEN = "YOURTOKENHERE"
bot = commands.Bot(command_prefix='.')
bot.remove_command('help')
githublink = "https://github.com/TheUserCreated/python-discord-tts"
message_queue = deque([])
db_pass = 'DBPASS'
db_user = 'DBUSER'


async def status_task():
    while True:
        game = discord.Game(f"In {len(bot.guilds)} servers.")
        await bot.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(30)


async def get_db_con():
    db = await asyncpg.connect(user=db_user, password=db_pass, database='postgres', host='127.0.0.1')

    return db


@bot.command()
async def blacklist(ctx):
    await ctx.send("Would you like to change the current blacklist status? Default is disabled.")
    channel = ctx.message.channel

    def check(m):
        if m.content.lower() == "yes":
            return True
        else:
            return False

    msg = await bot.wait_for('message', check=check, timeout=10)


@bot.command()
@commands.is_owner()
async def make_databases(ctx):
    guild_list = bot.fetch_guilds()
    db = await get_db_con()
    async for guild in guild_list:
        await db.execute("""CREATE TABLE guilds_conf (blacklist bool)""")
        ##TODO This is intended to make a place to store config items for each guild
        ## if someone wants to help please do
        ## i have no idea what im doing or how to use sql
        ## the goal is to store for each guild whether or not the blacklist is enabled
        ## whether or not the whitelist is enabled
        ## and the blacklist role and whitelist role
        ## whitelist role and blacklist role should be 0 or None if there is not one
        

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


@bot.event
async def on_ready():
    print("Bot online")
    bot.loop.create_task(status_task())


@bot.command()
@commands.is_owner()
async def eval_fn(ctx, *, cmd):
    """Evaluates input.

    Input is interpreted as newline seperated statements.
    If the last statement is an expression, that is the return value.

    Usable globals:
      - `bot`: the bot instance
      - `discord`: the discord module
      - `commands`: the discord.ext.commands module
      - `ctx`: the invokation context
      - `__import__`: the builtin `__import__` function

    Such that `>eval 1 + 1` gives `2` as the result.

    The following invokation will cause the bot to send the text '9'
    to the channel of invokation and return '3' as the result of evaluating

    >eval ```
    a = 1 + 2
    b = a * 2
    await ctx.send(a + b)
    a
    ```
    """
    fn_name = "_eval_expr"

    cmd = cmd.strip("` ")

    # add a layer of indentation
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

    # wrap in async def body
    body = f"async def {fn_name}():\n{cmd}"

    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)

    env = {
        'bot': ctx.bot,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        '__import__': __import__
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)

    result = (await eval(f"{fn_name}()", env))
    await ctx.send(result)


@bot.command()
async def join(ctx):
    try:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        return
    except(TypeError, AttributeError):
        await ctx.send("Either you are not in a voice channel, or I can't see the channel!")
        return


@bot.command()
async def leave(ctx):
    try:
        await ctx.voice_client.disconnect()
        return
    except(TypeError, AttributeError):
        await ctx.send("Can't disconnect from a voice channel when I'm not in one!")
        return


@bot.command()
async def stop(ctx):  # just an alias for leave
    await leave(ctx)


@bot.command()
async def say(ctx):
    if ctx.message.author.voice is None:
        await ctx.send("You must be in a Voice Channel to use that command!")
        return
    message = ctx.message.content[5:]
    usernick = ctx.message.author.display_name
    message = usernick + " says " + message
    try:
        vc = ctx.message.guild.voice_client
        if not vc.is_playing():
            tts = gTTS(message)
            f = TemporaryFile()
            tts.write_to_fp(f)
            f.seek(0)
            vc.play(discord.FFmpegPCMAudio(f, pipe=True))
        else:
            message_queue.append(message)
            while vc.is_playing():
                await asyncio.sleep(0.1)
            tts = gTTS(message_queue.popleft())
            f = TemporaryFile()
            tts.write_to_fp(f)
            f.seek(0)
            vc.play(discord.FFmpegPCMAudio(f, pipe=True))
    except(TypeError, AttributeError):
        try:
            tts = gTTS(message)
            f = TemporaryFile()
            tts.write_to_fp(f)
            f.seek(0)
            channel = ctx.message.author.voice.channel
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(f, pipe=True))
        except(AttributeError, TypeError):
            await ctx.send("I'm not in a voice channel and neither are you!")
        return
    f.close()


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Information and Commands", color=0x000000)
    embed.add_field(name=f"Commands", value="The commands are: \n .say \n .join \n .leave\n .help", inline=False)
    embed.add_field(name=f"Github Project Link",
                    value=f"And my github page is {githublink} ! \n Please feel free to contribute", inline=True)
    await ctx.send(embed=embed)


@bot.command()
@commands.is_owner()
async def die(ctx):
    game = discord.Game("")
    await bot.change_presence(status=discord.Status.offline, activity=game)
    bot.active = False
    await ctx.bot.logout()


bot.run(TOKEN)
