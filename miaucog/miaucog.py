from redbot.core import commands
import aiohttp, random
from montydb import (
    set_storage,
    MontyClient
); from datetime import datetime
from time import time


ext_api_url = 'https://api.thecatapi.com/v1/images/search?size=full'
set_storage("miau.db", storage="sqlite")
db_client = MontyClient("miau.db",
                        synchronous=1,
                        automatic_index=False,
                        busy_timeout=5000);
db = db_client.biralos; db_cats = db.cats; cats = set()
for cat_obj in tuple(db_cats.find()):
    cats.add(cat_obj['cat']);


async def get_cat(cached: bool = False):
    global cats
    if cached:
        if cats:
            return random.choice(tuple(cats))
    async with aiohttp.ClientSession() as session:
        async with session.get(ext_api_url) as resp:
            resp = await resp.json()
            cat_img_url = resp[0]['url']
            cats.add(cat_img_url)
            db_cats.insert_one({'cat': cat_img_url})
            return cat_img_url


async def get_cats(qty: int = 8, cached: bool = False):
    global cats
    if cached:
        if len(cats) >= qty:
            randomized_cats = list(cats)
            random.shuffle(randomized_cats)
            return randomized_cats[:qty]
    tmp_cats = []
    for _ in range(qty):
        cat_img_url = await get_cat()
        cats.add(cat_img_url)
        db_cats.insert_one({'cat': cat_img_url})
        tmp_cats.append(cat_img_url)
    return tmp_cats


class MiauCog(commands.Cog):
    """Miau miau"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def miau(self, ctx):
        """Miau miau maiu miau!"""
        cat = await get_cat()
        await ctx.message.reply(cat)

    @commands.command()
    async def miaumiau(self, ctx):
        """Miau miau maiu miau miau miau miau!"""
        cats = await get_cats(cached=True)
        await ctx.message.reply("MAMOOM!!")
        for cat in cats:
            await ctx.send(cat)
