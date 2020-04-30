import discord
import asyncio
from gtts import gTTS
from discord.ext import commands

TOKEN = 'YOURTOKENHERE'
client = commands.Bot(command_prefix='.')
client.remove_command('help')
githublink = "https://github.com/TheUserCreated/python-discord-tts"


@client.event
async def on_ready():
    print("Bot online")


@client.command()
async def join(ctx):
    try:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        return
    except(TypeError, AttributeError):
        await ctx.send("Either you are not in a voice channel, or I can't see the channel!")
        return


@client.command()
async def leave(ctx):
    try:
        await ctx.voice_client.disconnect()
        return
    except(TypeError, AttributeError):
        await ctx.send("Can't disconnect from a voice channel when I'm not in one!")
        return


@client.command()
async def say(ctx):
    message = ctx.message.content[5:]
    usernick = ctx.message.author.display_name
    tts = gTTS(usernick+" says " + message)
    tts.save('tts.mp3')
    try:
        vc = ctx.message.guild.voice_client
        try:
            vc.play(discord.FFmpegPCMAudio('tts.mp3'))
        except discord.errors.ClientException:
            await ctx.send(f"I can't say two things at once (and I don't have an audio queue yet!), please try again when "
                     "the current TTS message is done.\n If it's super long and spammy, try .leave .")
        return
    except(TypeError, AttributeError):
        try:
            channel = ctx.message.author.voice.channel
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio('tts.mp3'))
        except(AttributeError, TypeError):
            await ctx.send("I'm not in a voice channel and neither are you!")
        return


@client.command()
async def help(ctx):
    embed = discord.Embed(title="Information and Commands", color=0x000000)
    embed.add_field(name=f"Commands", value="The commands are: \n .say \n .join \n .leave\n .help", inline=False)
    embed.add_field(name=f"Github Project Link",
                    value=f"And my github page is {githublink} ! \n Please feel free to contribute", inline=True)
    await ctx.send(embed=embed)


client.run(TOKEN)
