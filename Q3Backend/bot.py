import discord
import os
import random
import interactions
from discord_slash import SlashCommand, SlashContext
from discord.ext import tasks
from dotenv import load_dotenv
import requests
import json

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
slash = SlashCommand(client, sync_commands=True)
members = []
wishlist = {}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}\n'
        )
    members = guild.members

@slash.slash(name="search", description="Search for media")
async def _search(ctx=SlashContext, *, media=None):
    await ctx.send(embed=discord.Embed(title="Fetching information", description="", color=0xff0000))
    link = "http://127.0.0.1:5000/api/details"
    try:
        retjson = requests.post(url=link, json={"slug": media})
        retjson = retjson.json()
        embed = discord.Embed(
            title=media.title(), description="", color=0xff0000)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        for c in retjson:
            embed.add_field(name=media, value=f"> Title: {c['name']}\n> Media Type: {c['media_type']}\n> \
                Description: {c['short_description']}\n> Genres: {c['genres']}\n> Ratings: {c['ratings']}\n> Review URL: {c['review_url']}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        notfound = discord.Embed(title="Media not found", color=0xff0000)
        return await ctx.send(embed=notfound)

@slash.slash(name="recommend", description="Recommends random media based on type and genre")
async def _recommend(ctx=SlashContext, *, type = None, genre = None):
    await ctx.send(embed=discord.Embed(title="Fetching information", description="", color=0xff0000))
    link = "http://127.0.0.1:5000/api/recommend"
    try:
        retjson = requests.post(url=link, json={"media_type": type, "genres": genre})
        retjson = retjson.json()
        embed = discord.Embed(
            title="Recommendations", description="", color=0xff0000)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        rand = [random.randint(0,len(retjson)) for i in range(5)]
        for c in rand:
             embed.add_field(name=type, value=f"> Title: {retjson[c]['name']}\n> Media Type: {retjson[c]['media_type']}\n> \
                 Description: {retjson[c]['short_description']}\n> Genres: {retjson[c]['genres']}\n> Ratings: {retjson[c]['ratings']}\n> Review URL: {retjson[c]['review_url']}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        notfound = discord.Embed(title="Media not found", color=0xff0000)
        return await ctx.send(embed=notfound)

@slash.slash(name="publisher", description="Searches media based on media type and publisher")
async def _publisher(ctx=SlashContext, *, type = None, publisher = None):
    await ctx.send(embed=discord.Embed(title="Fetching information", description="", color=0xff0000))
    link = "http://127.0.0.1:5000/api/publisher"
    try:
        retjson = requests.post(url=link, json={"media_type": type, "published_by": publisher})
        retjson = retjson.json()
        print(retjson)
        embed = discord.Embed(
            title="Results", description="", color=0xff0000)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        rand = [random.randint(0,len(retjson)) for i in range(5)]
        for c in rand:
             embed.add_field(name=type, value=f"> Title: {retjson[c]['name']}\n> Media Type: {retjson[c]['media_type']}\n> \
                 Description: {retjson[c]['short_description']}\n> Genres: {retjson[c]['genres']}\n> Ratings: {retjson[c]['ratings']}\n> Review URL: {retjson[c]['review_url']}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        notfound = discord.Embed(title="Media not found", color=0xff000)
        return await ctx.send(embed=notfound)

@slash.slash(name="add_media", description="Adds media to your wishlist")
async def _add(ctx=SlashContext, *, media=None):
    await ctx.send(embed=discord.Embed(title="Fetching information", description="", color=0xff0000))
    link = "http://127.0.0.1:5000/api/details"
    try:
        retjson = requests.post(url=link, json={"slug": media})
        retjson = retjson.json()
        embed = discord.Embed(
            title=media.title(), description="", color=0xff0000)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        for c in retjson:
            print(c)
            embed.add_field(name=media, value=f"> Title: {c['name']}\n> Media Type: {c['media_type']}\n> \
                Description: {c['short_description']}\n> Genres: {c['genres']}\n> Ratings: {c['ratings']}\n> Review URL: {c['review_url']}", inline=False)
        await ctx.send(embed=embed)
        wishlist[ctx.author].append(c)
    except KeyError:
        wishlist[ctx.author] = []
        wishlist[ctx.author].append(c)
    except Exception as e:
        print(e)
        notfound = discord.Embed(title="Media not found", color=0x00ff00)
        return await ctx.send(embed=notfound)

@slash.slash(name="view_media", description="View media in your wishlist")
async def _view(ctx=SlashContext):
    embed = discord.Embed(
            title="Wishlist", description="", color=0xff0000)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    array = wishlist.get(ctx.author)
    for c in array:
        print(c)
        embed.add_field(name=c['name'], value=f"> Title: {c['name']}\n> Media Type: {c['media_type']}\n> \
                Description: {c['short_description']}\n> Genres: {c['genres']}\n> Ratings: {c['ratings']}\n> Review URL: {c['review_url']}", inline=False)
    await ctx.send(embed=embed)

@slash.slash(name="franchise", description="Search a franchise by media type")
async def _franchise(ctx=SlashContext, *, franchise = None, media = None):
    await ctx.send(embed=discord.Embed(title="Fetching information", description="", color=0xff0000))
    link = "http://127.0.0.1:5000/api/mediafranchise"
    try:
        retjson = requests.post(url=link, json={"franchise": franchise, "media_type": media})
        retjson = retjson.json()
        embed = discord.Embed(
            title="Franchises", description="", color=0xff0000)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        rand = [random.randint(0,len(retjson)) for i in range(2)]
        for c in rand:
             embed.add_field(name=franchise, value=f"> Title: {retjson[c]['name']}\n> Media Type: {retjson[c]['media_type']}\n> \
                 Description: {retjson[c]['short_description']}\n> Genres: {retjson[c]['genres']}\n> Ratings: {retjson[c]['ratings']}\n> Review URL: {retjson[c]['review_url']}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        notfound = discord.Embed(title="Media not found", color=0x00ff00)
        return await ctx.send(embed=notfound)

client.run('ODk5NTMxNTM5NTkzOTY5Njc0.GMJrIB.z2p8am7Yk0k-mZfaVZOA9NVYhaIELMVS272CLc')