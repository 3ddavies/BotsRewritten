import discord
import datetime
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import shutil

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

@koneko.command(pass_context=True, aliases=["pl"])
async def play(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./soqu")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("soqu"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("soqu") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir("./soqu")
    try:
        Queue_folder = "./soqu"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("Getting everything ready now")

    voice = get(koneko.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")



@koneko.command(pass_context=True, aliases=["pa"])
async def pause(ctx):
    voice = get(koneko.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.pause()
        await ctx.send("Pausing your lovely tunes.")

    else:
        await ctx.send("I'm not playing anything, why do you want me to shut up so badly?!")

@koneko.command(pass_context=True, aliases=["r"])
async def resume(ctx):
    voice = get(koneko.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        voice.resume()
        await ctx.send("Resuming music. What a BOP!")

    else:
        await ctx.send("I'm flattered you like hearing me so much, but I don't have anything to resume :wink:")

@koneko.command(pass_context=True, aliases=["s"])
async def stop(ctx):
    voice = get(koneko.voice_clients, guild=ctx.guild)

    queues.clear()

    if voice and voice.is_playing():
        voice.stop()
        await ctx.send("I'll stop playing that.")

    else:
        await ctx.send("I'm not playing anything, why do you want me to shut up so badly?!")

queues = {}

@koneko.command(pass_context=True, aliases=["que"])
async def queue(ctx, url: str):
    qif = os.path.isdir("./soqu")

    if qif is False:
        os.mkdir("soqu")

    dp=os.path.abspath(os.path.realpath("soqu"))
    qn=len(os.listdir(dp))+1
    aq=True

    while aq == True:
        if qn in queues:
            qn+=1
        else:
            aq=False
            queues[qn]=qn

    qp=os.path.abspath(os.path.realpath("soqu")+f"\s{qn}.%(ext)s")

    ytdl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': qp,
        'postprocessors': [{
            "key": 'FFmpegExtractAudio',
            "preferredcodec": 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        print("Downloading...\n")
        ydl.download([url])
    await ctx.send(f"Adding item to the queue. {qn} items in queue total.")

@koneko.command()
async def ping(ctx):
    await ctx.send(f""":ping_pong: Pong! ({round(koneko.latency, 1)}ms)""")

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
    await ctx.send(f"The time is {cdat.hour}:{cdat.minute}:{cdat.second} and the date is {cdat.day}/{cdat.month}/{cdat.year}")


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
async def on_member_join(ctx,member):
    for channel in member.server.channels:
        if channel == "general":
            await ctx.send(f"""Welcome, {member.mention}! I'm so glad you're here :sparkling_heart:""")


@koneko.event
async def on_ready():
    print("I am up and running!!")



kont, kurt = read_tokens()

koneko.run(kont)
kuroka.run(kurt)
