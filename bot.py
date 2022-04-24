import discord
import os
import random
import interactions
from discord_slash import SlashCommand, SlashContext
from discord.ext import tasks
from dotenv import load_dotenv
from itsdangerous import exc
import requests
import json

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
slash = SlashCommand(client, sync_commands=True)
members = []

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
        retjson = requests.post(url=link, json={'slug': media})
        embed = discord.Embed(
            title=media.title(), description="", color=0xff0000)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        for c in retjson:
            print(c)
            embed.add_field(name=media, value=f"> Title: {c['name']}\n> Media Type: {c['media_type']}\n> \
                Description: {c['short_description']}\n> Genres: {c['genres']}\n> Ratings: {c['ratings']}\n> Review URL: {c['review_url']}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        notfound = discord.Embed(title="Course not found", color=0x00ff00)
        return await ctx.send(embed=notfound)


client.run(os.environ['TOKEN'])