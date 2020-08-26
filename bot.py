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

koneko = discord.Client()
kuroka = discord.Client()

@koneko.event
async def on_message(message):
    msg=message.content.split(" ")
    if msg[0][0]=="!":#checks for appropriate prefix
        cmdn=msg[0][1:]#gets the name of the command
        largs = msg[1:]#arguments passed with the command
        "message.guild"

        if cmdn == "ping":
            await message.channel.send(":ping_pong: Pong!")

        elif cmdn == "pwd":
            await message.channel.send(os.getcwd())

        elif cmdn == "ls":
            await message.channel.send("Contents of Directory \""+os.getcwd()+"\":")
            dirc = os.listdir(os.getcwd()) #directory contents array
            splitnum = 15
            dircf = [dirc[i * splitnum:(i + 1) * splitnum] for i in range((len(dirc) + splitnum - 1) // splitnum)]

            for i in dircf:
                await message.channel.send('\n'.join(i))
        elif cmdn == "cd":
            try:
                os.chdir(largs[0])
                await message.channel.send("Current working directory has been changed to " + os.getcwd())
            except TypeError:
                await message.channel.send("Invalid Directory")

        elif cmdn == "ostimes":
            await message.channel.send(os.times())

        elif cmdn == "time":
            cdat = datetime.datetime.now()
            await message.channel.send("The time is "+str(cdat.hour)+":"+str(cdat.minute)+":"+str(cdat.second)+" and the date is "+str(cdat.day)+"/"+str(cdat.month)+"/"+str(cdat.year))

        elif cmdn == "ppap":
            await message.channel.send(f"""Just for you, {message.author.mention}:""")
            await message.channel.send("https://www.youtube.com/watch?v=0E00Zuayv9Q")

        elif cmdn == "ppap2020":
            await message.channel.send(f"""Stay safe, {message.author.mention}!!""")
            await message.channel.send("https://www.youtube.com/watch?v=WKfolJv6Kx8")

        else:
            await message.channel.send("Sorry hun, I don't quite know what you're on about. I'll tell you more about what I can do with !help")
            await message.channel.send(":stuck_out_tongue_winking_eye:")

@koneko.event
async def on_member_join(member):
    for channel in member.server.channels:
        if channel == "general":
            await channel.send(f"""Welcome, {member.mention}! I'm so glad you're here :sparkling_heart:""")

@koneko.event
async def on_ready():
    print("I am up and running!!")

"""
@koneko.command()
async def ping(*args):
    await koneko.send_message(":ping_pong: Pong!")
"""

kont, kurt = read_tokens()

koneko.run(kont)
kuroka.run(kurt)