import discord
from gtts import gTTS
from discord.ext import commands

TOKEN = 'YOURTOKENHERE'
client = commands.Bot(command_prefix='.')
client.remove_command('help')


@client.event
async def on_ready():
    print("Bot online")


@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    try:
        vc = await channel.connect()
        return
    except:
        await ctx.send("I can't be in two voice channels at once! Disconnect me from the other one first!")
        return


@client.command()
async def leave(ctx):
    try:
        await ctx.voice_client.disconnect()
        return
    except:
        await ctx.send("Can't disconnect from a voice channel when I'm not in one!")
        return


@client.command()
async def say(ctx):
    message = ctx.message.content[5:]
    tts = gTTS(message)
    tts.save('tts.mp3')
    try:
        vc = ctx.message.guild.voice_client
        vc.play(discord.FFmpegPCMAudio('tts.mp3'))
        return
    except(TypeError, AttributeError):
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio('tts.mp3'))
        return


@client.command()
async def help(ctx):
    embed = discord.Embed(title="Information and Commands")
    embed.add_field(name="Information", value=f"The commands are: \n .say \n .join \n .leave")
    await ctx.send(embed=embed)


client.run(TOKEN)
