import discord
from discord.ext import commands
import random
from random import randint
import aiohttp
import asyncio
import re

bot=commands.Bot(command_prefix=".")

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------------")

@bot.command(pass_context=True)
async def news(ctx):
    await bot.delete_message(ctx.message)
    async with aiohttp.ClientSession() as client:
        async with client.get('https://www.epicgames.com/paragon/api/blog/getPosts') as resp:
            data1=await resp.json()
            url=data1["blogList"][0]["url"]
            await bot.say("https://www.epicgames.com/paragon{}".format(url))
            
@bot.command(pass_context=True)
async def patchnotes(ctx):
    await bot.delete_message(ctx.message)
    async with aiohttp.ClientSession() as client:
        async with client.get('https://www.epicgames.com/paragon/api/blog/getPosts') as resp:
            data1=await resp.json()
            for i in data1["blogList"]:
                if "Release Notes" in i["title"]:
                    url=i["url"]
                    break
            await bot.say("https://www.epicgames.com/paragon{}".format(url))

@bot.command(pass_context=True)
async def stats(ctx,*,name:str):
    """Type '.stats name' to return agora.gg current season stats"""
    await bot.delete_message(ctx.message)
    async with aiohttp.ClientSession() as client:
        async with client.get('https://api.agora.gg/players/search/{}?lc=en&ssl=true'.format(name)) as resp:
            data1=await resp.json()
            try: name=data1["data"][0]["name"]
            except:
                await bot.say("{} not found".format(name))
                return
            id1=data1["data"][0]["id"]
            async with client.get("https://api.agora.gg/players/{}?season=2&lc=en&ssl=true".format(id1)) as final_resp:
                data2=await final_resp.json()

    stats1 = data2['data']['stats']
    if stats1:
        for i in data2["data"]["stats"]:
            if i["mode"]==4:
                elo=i["elo"]
                rank=i["rank"]
                kda=float((i["kills"]+i["assists"])/i["deaths"])
                gamesPlayed=i["gamesPlayed"]
                losses=float((i["gamesPlayed"])-i["wins"])
                winloss=float((i["wins"]/i["gamesPlayed"])*100)
                towers=i["towers"]
                kills=i["kills"]
                assists=i["assists"]
                deaths=i["deaths"]
                wins=i["wins"]
                towerspergame=float(i["towers"]/i["gamesPlayed"])
                await bot.say("**{name} current season stats**:\nELO: {elo:0.0f}\nWin%: {winloss:.2f} | Games: {gamesPlayed} | Wins: {wins} | Losses: {losses:0.0f}\nKDA: {kda:0.2f} | Kills: {kills} | Deaths: {deaths} | Assists: {assists}\nTowers Per Game: {towerspergame:0.2f} | Towers: {towers}\nRank: {rank}".format(name=name,gamesPlayed=gamesPlayed,winloss=winloss,elo=elo,kda=kda,towerspergame=towerspergame,wins=wins,rank=rank,losses=losses,towers=towers,kills=kills,deaths=deaths,assists=assists))    
    else:
        await bot.say("**{}** is private on agora.gg".format(name))

@bot.command(pass_context=True)
async def elo(ctx,*,name:str):
    """Type '.elo name' to return agora.gg current season ELO"""
    await bot.delete_message(ctx.message)
    async with aiohttp.ClientSession() as client:
        async with client.get('https://api.agora.gg/players/search/{}?lc=en&ssl=true'.format(name)) as resp:
            data1=await resp.json()
            try: name=data1["data"][0]["name"]
            except:
                await bot.say("{} not found".format(name))
                return
            id1=data1["data"][0]["id"]
            async with client.get("https://api.agora.gg/players/{}?season=2&lc=en&ssl=true".format(id1)) as final_resp:
                data2=await final_resp.json()
                
    stats1 = data2['data']['stats']
    if stats1:
        for i in data2["data"]["stats"]:
            if i["mode"]==4:
                elo=i["elo"]
                await bot.say("**{name}** - ELO: {elo:0.0f}".format(name=name,elo=elo))
    else:
        await bot.say("**{}** is private on agora.gg".format(name))

@bot.command(pass_context=True)
async def kda(ctx,*,name:str):
    """Type '.kda name' to return agora.gg current season KDA"""
    await bot.delete_message(ctx.message)
    async with aiohttp.ClientSession() as client:
        async with client.get('https://api.agora.gg/players/search/{}?lc=en&ssl=true'.format(name)) as resp:
            data1=await resp.json()
            try: name=data1["data"][0]["name"]
            except:
                await bot.say("{} not found".format(name))
                return
            id1=data1["data"][0]["id"]
            async with client.get("https://api.agora.gg/players/{}?season=2&lc=en&ssl=true".format(id1)) as final_resp:
                data2=await final_resp.json()

    stats1 = data2['data']['stats']
    if stats1:
        for i in data2["data"]["stats"]:
            if i["mode"]==4:
                kda=float((i["kills"]+i["assists"])/i["deaths"])
                await bot.say("**{name}** - KDA: {kda:0.2f}".format(name=name,kda=kda))
    else:
        await bot.say("**{}** is private on agora.gg".format(name))

@bot.command(pass_context=True)
async def coinflip(ctx,*coinflip : str):
    """Type '.coinflip' and the bot will randomly choose between 'heads' or 'tails'"""
    await bot.delete_message(ctx.message)
    coinflip = ['Heads!', 'Tails!']
    await bot.say(random.choice(coinflip))

            
bot.run("###PUT BOT KEY HERE###")
