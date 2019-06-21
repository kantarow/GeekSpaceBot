from discord.ext import commands

import traceback
import json
import logging


INITIAL_EXTENSIONS = (
    'extensions.genembed',
)
logger = logging.getLogger('gsbot')


class GSBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='g!')

        with open('config/config.json') as f:
            self.config = json.load(f)

        for ext in INITIAL_EXTENSIONS:
            try:
                self.load_extension(ext)
            except Exception:
                traceback.print_exc()

    async def start(self):
        await super().start(self.config['Token'])
