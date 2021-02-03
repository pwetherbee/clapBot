#bot.py
import os
import ssl
import discord
import asyncio
import json
import random
import wikiquote
from time import sleep
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from discord.ext import commands

#from azure.cognitiveservices.search.imagesearch import ImageSearchClient
#from msrest.authentication import CognitiveServicesCredentials

#subscription_key = "4535d83c67544af3bf4fd58994ca578a"
#subscription_endpoint = "https://discordbotimagesearch.cognitiveservices.azure.com/"

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN", "token does not exist")
GUILD = os.getenv("DISCORD_GUILD", "guild name does not exist")
#subscription_key = os.getenv("SUBSCRIPTION_KEY", "subscription key does not exist") #found on microsoft azure
#subscription_endpoint = os.getenv("SUBSCRIPTION_ENDPOINT", "subscription endpoint does not exist")

#client = ImageSearchClient(endpoint=subscription_endpoint, credentials=CognitiveServicesCredentials(subscription_key)) #connect to image client

bot = commands.Bot(command_prefix = "cl")

#specify path to audio files on computer
audioPath = "G:/My Drive/discordMp3s/" #test destination is "C:/Users/Patrick Wetherbee/Desktop/testMp3s/"
popTrackPath = 'tracker/popularity.txt'
userAcctPath = 'tracker/accounts.txt'
h = 'ap' #hack I used to create generic commands



@bot.event
async def on_ready():
    print(f"{bot.user} has connected to discord!")  
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f"Bot is connected to the {guild} server")

'''
Command functions (be sure to define with @bot.command decorator and async keyword and call with await keyword)
'''

'''
Audio Commands: Play, RandomPlay, Stop
'''
#main command that plays mp3s, also includes help command that returns all available mp3 filenames that can be played
@bot.command(name = h)
async def playIt(ctx, *args):
    params=None
    filters=None
    if len(args) > 1:
        arg = str(args[0])
        params = args[1:]
    else:
        arg = str(args[0])
    if params:
        filters = filter(params)
    if arg == 'help':
        return await listMp3s(ctx)
    if isValidMp3(arg):
        await ctx.message.add_reaction('👏')
        addIndexToFile(arg + '.mp3', popTrackPath)
        addIndexToUsers(str(ctx.message.author))
        await ctx.message.add_reaction(assignTier(arg + '.mp3'))
        await playmp3(ctx, arg + '.mp3', filters)
    else:
        await ctx.message.add_reaction('⁉')

#command for playing a randomly chosen mp3
@bot.command(name = h + 'r')
async def randomMp3(ctx):
    await ctx.message.add_reaction('🎲')
    x = random.choice(list(getMp3s()))
    addIndexToFile(x)
    await playmp3(ctx, x)



#command for stopping audio and disconnecting bot from voice channel, command will be clapstop
@bot.command(name = h + 'stop')
async def stop(ctx):
    await ctx.message.add_reaction('✋')
    for x in bot.voice_clients:
        if(x.guild == ctx.message.guild):
            return await x.disconnect()
    return ctx.send('I am not in a voice channel on this server!')



'''
Bot Info Commands: Search, numplays, new and top
'''

#main command for searching mp3s command will be claps
@bot.command(name = h + 's')
async def searchMp3(ctx, arg=''):
    searchResults = search(arg)
    await ctx.message.add_reaction('🔍')
    if not searchResults:
        await ctx.message.add_reaction('😢')
        await ctx.send(f'```No results found for {arg}```')
        return
    popDict = readFile() #reads popularity text file
    withTiers = getTiersAndPlays(popDict, searchResults[:50])
    await ctx.send(formatMessage(arg,withTiers))

#show most played mp3s, command will be claptop
@bot.command(name=h +'top')
async def showRanks(ctx, arg='10'):
    if arg == 'users':
        #do something
        await ctx.message.add_reaction('👏')
        accounts = readFile(userAcctPath)
        top = [a.split('#')[0].ljust(23) + str(k['playCount']) for a, k in sorted(accounts.items(), key=lambda item: item[1]['playCount'])][::-1]
        await ctx.send(formatMessage('TopUsers', top))
        return
    try:
        arg = int(arg)
    except ValueError:
        await ctx.message.add_reaction('⁉')
        return
    if arg > 75:
        await ctx.send('The limit for top is 75')
        arg = 75
    await ctx.message.add_reaction('👏')
    popDict = readFile()
    ranks = getRanks(popDict) #reverse the rankings for top down order
    allInfo = getTiersAndPlays(popDict,ranks[:arg])
    await ctx.send(formatMessage('Top',allInfo))

#show newest and unplayed mp3s
@bot.command(name=h + 'new')
async def showNew(ctx):
    popDict = readFile()
    allFiles = getRanks(popDict, 'bottom')
    onlyNew = getTiersAndPlays(popDict,allFiles,'🆕')
    await ctx.send(formatMessage('New', onlyNew))

    
#returns info on the user calling the command
@bot.command(name=h + 'me')
async def userInfo(ctx):
    await ctx.message.add_reaction('👏')

    user = str(ctx.message.author)

    accountDict = readFile('tracker/accounts.txt')
    print(accountDict)

    createAccountEntry(user)
    playInfo = accountDict.get(user).get('playCount')
    print(playInfo)
    await ctx.send(f'You have clapped {playInfo} cheeks')

@bot.command(name=h + 'fx')
async def dislpaySoundFX(ctx):
    await ctx.message.add_reaction('👏')
    await ctx.send(f'spam, weird, radio, fast, slow, reverse')

@bot.command(name=h + ' rwiki')
async def on_message(ctx):
    response = 'https://en.wikipedia.org/wiki/Special:Random'
    await ctx.message.add_reaction('👏')
    await ctx.send(response)

"""
Helper Functions - Be sure to call with the await keyword(decorator?) if they are commands
"""
def getMp3s(path = audioPath):
    print('Searching files in directory...', path, '\n')
    files = set(os.listdir(path))
    return files

def formatMessage(arg, items):
    #TODO: Fix this entire mess of strings using proper dynamic formatting
    bar = '-'*27 + '\n'
    message = f'Showing search results for {arg}: \n\nName          Tier    Plays\n' + bar + '\n'.join(items)
    return f"```{message}```"

def isValidMp3(fileName):
    print(fileName + '.mp3')
    return fileName + '.mp3' in getMp3s(audioPath)

async def listMp3s(ctx):
    await ctx.message.add_reaction('👏')
    mp3List = sorted(list(getMp3s()))
    message = '\n'.join([mp3[:-4] for mp3 in mp3List]) #cut out .mp3 tag
    message = 'Below are all of the available Mp3s, try them out with the command clap *mp3Name* ! \n \n' + message
    message += '\nBelow are all of the available sound fx, write them after the mp3 name like *clap mp3Name effectName* !\n\nspam, weird, fast, slow, reverse'
    await ctx.send(f"```{message}```")
    

#preliminary basic search function
def search(keyword):
    results1 = set()
    results2 = set()
    for filename in getMp3s():
        if filename.startswith(keyword):
            results1.add(filename[:-4])
        elif len(keyword) > 1 and keyword in filename:
            results2.add(filename[:-4])
    return sorted(list(results1)) + sorted(list(results2))


async def playmp3(ctx, path, filters=None): #plays an mp3 file given the path (root is same as py file)
    path = audioPath + path
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    def dcFromChannel(error):
        coroutine = voice.disconnect()
        future = asyncio.run_coroutine_threadsafe(coroutine, bot.loop)
        try:
            future.result()
        except:
            pass
    source = FFmpegPCMAudio(path, executable = 'C:/FFMPEG/ffmpeg.exe', options = filters)
    player = voice.play(source, after=dcFromChannel)
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.volume = 1


def filter(keywords):
    filterComms = '-filter_complex "volume = 1'
    for keyword in keywords:
        chorus=',chorus=0.5:0.9:50|60|40:0.4|0.32|0.3:0.25|0.4|0.3:2|2.3|1.3'
        if keyword == 'spam': filterComms += ',volume=20 , bass=20,dcshift=0.8, volume=0.4'
        if keyword == 'slow': filterComms += ',atempo=0.5'
        if keyword == 'fast': filterComms += ',atempo=1.5'
        if keyword == 'superfast': filterComms += ',atempo=2.5'
        if keyword == 'radio': filterComms += ',bandpass,acrusher=1:1:50:0:log,bandpass'
        if keyword == 'weird': filterComms += ',flanger'
        if keyword == 'reverse': filterComms += ',areverse'
        if keyword == 'chorus': filterComms += chorus*20
    return filterComms + '"'


def get_quote(keyword): #returns a quote from wikiquote for a given name or keyword
    quotes = wikiquote.quotes(keyword)
    quote = random.choice(quotes)
    return quote

def readFile(path = popTrackPath):
    with open(path, 'r') as file:
        return json.loads(file.read())

def addIndexToFile(key, path = popTrackPath):
    with open(path, 'r') as file:
        #print(file.read())
        tempDict = json.loads(file.read())
        #print(tempDict)
        if tempDict.get(key):
            tempDict[key] += 1
        else:
            tempDict[key] = 1  
    with open(path, 'w') as file:
        file.write(json.dumps(tempDict))
        file.close()

def addIndexToUsers(user, path='tracker/accounts.txt'):
    with open(path, 'r') as file:
        #print(file.read())
        accountDict = json.loads(file.read())
        if not accountDict.get(user):
            accountDict[user] = {'playCount':0} #init new user entry
        if accountDict[user].get('playCount'):
            accountDict[user]['playCount'] += 1
        else:
            accountDict[user]['playCount'] = 1  
    with open(path, 'w') as file:
        file.write(json.dumps(accountDict))
        file.close()

def createAccountEntry(user,path ='tracker/accounts.txt'):
    with open(path, 'r') as file:
        accountDict = json.loads(file.read())
        if not accountDict.get(user):
            accountDict[user] = {'playCount':0} #init new user entry
        else:
            return
    with open(path, 'w') as file:
        file.write(json.dumps(accountDict))
        file.close()

    
def getRanks(popDict, order = 'top'):
    ranks = [f[:-4] for f, k in sorted(popDict.items(), key = lambda item: item[1])]
    if order == 'bottom':
        return ranks
    return ranks[::-1] #reverse order to show top ranks


def checkTier(plays):
    if not plays or plays < 5: return '🆕'  
    if plays < 10: return '🥝' 
    if plays < 25: return '🥪' 
    if plays < 50: return '🥉' 
    if plays < 75: return '🥈'
    if plays < 100: return '💯'
    if plays < 125: return '🥇'
    if plays < 150: return '💎'
    if plays < 200: return '👑'
    if plays < 300: return '🥓'
    if plays < 400: return '🔥'
    if plays < 500: return '😩'
    if plays < 600: return '☠'
    return '👽'

def assignTier(key):
    return checkTier(readFile()[key])

def getTiersAndPlays(fileDict, searchResults, filter=None):
    allInfo = []
    for result in searchResults:
        res = result.ljust(15) #build result and pad
        tier = checkTier(fileDict.get(result + '.mp3')).ljust(7) #build tier emoji and pad
        numPlays = str(fileDict.get(result + '.mp3', '0')) #build num plays
        allInfo.append(res + tier + numPlays) #combine all elements line by line
    if filter:
        return [line for line in allInfo if filter in line]
    return allInfo


bot.run(TOKEN)


'''


#TODO: add these functions:

function that returns the number of plays for a given mp3

function that returns the number of plays and tiers for all mp3s (add to search and help functions?)

'''


#TODO: add a theshold function for large servers, add funtion using pytube to download youtube clips with timestamps and custom titles
#add support for different file types such as aac and m4a files