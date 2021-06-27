from os import path
from configparser import ConfigParser
import anirocks
from pyrogram import Client
from anirocks import Client as AniRocks


config_file = "bot.ini"

config = ConfigParser()
config.read(config_file)

anirocks = AniRocks(base_url=config.get('api', 'url'))

class bot(Client):
    def __init__(self, name):
        name = name.lower()
        plugins = {'root': path.join(__package__, 'plugins')}
        super().__init__(
            name,
            config_file=config_file,
            workers=16,
            plugins=plugins,
            workdir="./",
        )
    async def start(self):
        await super().start()
        print("bot started. Hi.")

    async def stop(self, *args):
        await super().stop()
        print("bot stopped. Bye.")

    async def get_genres(self):
        return (await anirocks.genrelist()).list
    
    async def get_genre(self, type, page):
        return (await anirocks.genre(type=type, page=page)).results
    
    async def search_anime(self, query: str):
        return (await anirocks.search(query=query, page=1)).results
    
    async def anime_details(self, anime_id: str):
        return (await anirocks.details(anime_id))
    
    async def fetch_episodes(self, anime_id, episode):
        return (await anirocks.watch(anime_id, episode))
