import time
from time import sleep
from itertools import cycle
import discord
import asyncio

from discord.ext import tasks

client = discord.Client()




@tasks.loop(minutes=5.0)
async def wypiszPbf():
    await client.wait_until_ready()
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name == 'aktywne-sesje':
                from Scraper import tekstPBF
                for item in tekstPBF():
                    lista = item
                    await client.get_channel(channel.id) \
                        .send(lista)
                    await asyncio.sleep(5)


@tasks.loop(minutes=5.0)
async def wypiszForum():
    await client.wait_until_ready()
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name == 'tawerna-rpg':
                from Scraper import tekstForum
                for item in tekstForum():
                    lista = item
                    await client.get_channel(channel.id) \
                        .send(lista)
                    await asyncio.sleep(5)


@tasks.loop(hours=1.0)
async def wypiszRss():
    await client.wait_until_ready()
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name == 'tawerna-rpg':
                from Scraper import tekstRSS
                for item in tekstRSS():
                    lista = item
                    await client.get_channel(channel.id) \
                        .send(lista)
                    await asyncio.sleep(5)


async def status(nowy_status=""):
    await client.wait_until_ready()
    from OperacjeNaPlikach import opis, nowy_opis
    from itertools import cycle
    if not nowy_status:
        messages = cycle(opis())
        while not client.is_closed():
            opis = next(messages)
            await client.change_presence(status=discord.Status.idle, activity=discord.Game(opis))
            import asyncio
            await asyncio.sleep(300)
    elif nowy_status:
        messages = cycle(opis())
        while not client.is_closed():
            opis = next(messages)
            await client.change_presence(status=discord.Status.idle, activity=discord.Game(opis))
            import asyncio
            await asyncio.sleep(300)


@client.event
async def on_ready():
    print(f'Zalogowano jako: {client.user.name}')
    print(f"Id użytkownika: {client.user.id}")
    print('----------------------------------')


# Tu trzeba wstawić token 0auth
def OdczytajToken():
    with open("Dane/token_0auth.txt", "r") as token:
        odczytany_token = token.readlines()
        return odczytany_token[0].strip()


client.loop.create_task(status())
wypiszPbf.start()
wypiszForum.start()
wypiszRss.start()
client.run(OdczytajToken())
