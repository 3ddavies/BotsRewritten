import discord
import datetime
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os

def read_tokens():
    with open("tokens.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip(), lines[1].strip()


koneko = commands.Bot(description="A Discord Bot!", command_prefix="!", pm_help=True)
kuroka = commands.Bot(description="Another Discord Bot!", command_prefix="-", pm_help=True)


@koneko.command(pass_context=True, aliases=["j","summon"])
async def join(ctx):
    global voice
    channel=ctx.message.author.voice.channel#voice channel of requesting user
    voice = get(koneko.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():#checks if the bot needs to change voice channels
        await voice.move_to(channel)#move to new voice channel

    else:#not in a voice channel
        voice = await channel.connect()#join the voice channel requesting user is in

    await ctx.send(f"""As you wish, {ctx.message.author.mention}. Connected to voice channel \"{channel}\".""")

@koneko.command(pass_context=True, aliases=["l","fuckoff"])
async def leave(ctx):
    global voice
    channel = ctx.message.author.voice.channel  # voice channel of requesting user
    voice = get(koneko.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():#checks if the bot is connected
        if ctx.author.voice.channel == ctx.voice_client.channel:  #if requesting user is in same vc as bot
            await voice.disconnect()
            await ctx.send(f"""Leaving the voice channel \"{channel}\". see you next time {ctx.message.author.mention}! :kissing_heart:""")

        else:#cmd issuer is in different or no vc
            await ctx.send(f"""Hey {ctx.message.author.mention}! You aren't even in \"{ctx.voice_client.channel}\" with me, why do you want me to leave so badly?!""")
    else:
        await ctx.send("I'm not connected to a voice channel silly!")

@koneko.command(pass_context=True, aliases=["p"])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:#if there is an existing song file
            os.remove("song.mp3")
    except PermissionError:
        print("Song is being played currently, can't delete.")
        await ctx.send("I'm already playing something!!")
        return

    await ctx.send("Just finishing up!")

    voice = get(koneko.voice_clients, guild=ctx.guild)

    ytdl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            "key": 'FFmpegExtractAudio',
            "preferredcodec": 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        print("Downloading...\n")
        ydl.download([url])

    for f in os.listdir("./"):
        if f.endswith('.mp3'):
            name=f
            os.rename(f, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"Done playing {name}."))
    voice.source=discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nn = name.rsplit("-",2)
    await ctx.send(f"playing {nn}")


@koneko.command()
async def ping(ctx):
    await ctx.send(":ping_pong: Pong!")

@koneko.command()
async def pwd(ctx):
    await ctx.send(os.getcwd())

@koneko.command()
async def ls(ctx):
    await ctx.send("Contents of Directory \"" + os.getcwd() + "\":")
    dirc = os.listdir(os.getcwd())  # directory contents array
    splitnum = 15
    dircf = [dirc[i * splitnum:(i + 1) * splitnum] for i in range((len(dirc) + splitnum - 1) // splitnum)]

    for i in dircf:
        await ctx.send('\n'.join(i))

@koneko.command()
async def cd(ctx, dtgt):
    try:
        os.chdir(dtgt)
        await ctx.send("Current working directory has been changed to " + os.getcwd())
    except TypeError:
        await ctx.send("Invalid Directory")

@koneko.command()
async def ostimes(ctx):
    await ctx.send(os.times())

@koneko.command()
async def time(ctx):
    cdat = datetime.datetime.now()
    await ctx.send("The time is " + str(cdat.hour) + ":" + str(cdat.minute) + ":" + str(cdat.second) + " and the date is " + str(cdat.day) + "/" + str(cdat.month) + "/" + str(cdat.year))


@koneko.command()
async def ppap(ctx):
    await ctx.send(f"""Just for you, {ctx.message.author.mention}:""")
    await ctx.send("https://www.youtube.com/watch?v=0E00Zuayv9Q")


@koneko.command()
async def ppap2020(ctx):
    await ctx.send(f"""Stay safe, {ctx.message.author.mention}!!""")
    await ctx.send("https://www.youtube.com/watch?v=WKfolJv6Kx8")


@koneko.command(hidden=True)
async def budski(ctx):
    await ctx.send("Working")
"""
except discord.ext.commands.errors.CommandNotFound:
    await ctx.send("Unknown command.")
"""

"""
@koneko.event
async def on_message(message):
    msg = message.content.split(" ")
    if msg[0][0] == "!":  # checks for appropriate prefix
        cmdn = msg[0][1:]  # gets the name of the command
        largs = msg[1:]  # arguments passed with the command
        "message.guild"



        else:
            await message.channel.send(
                "Sorry hun, I don't quite know what you're on about. I'll tell you more about what I can do with !help")
            await message.channel.send(":stuck_out_tongue_winking_eye:")
"""

@koneko.event
async def on_member_join(member):
    for channel in member.server.channels:
        if channel == "general":
            await channel.send(f"""Welcome, {member.mention}! I'm so glad you're here :sparkling_heart:""")


@koneko.event
async def on_ready():
    print("I am up and running!!")



kont, kurt = read_tokens()

koneko.run(kont)
kuroka.run(kurt)
