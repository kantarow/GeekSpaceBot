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

    def load_config(self, filepath: str) -> dict:
        try:
            with open(filepath, mode='r', encoding='utf8') as f:
                return json.load(f)
        except OSError:
            logger.error('Configuration file is not found.')
            self.save_config(filepath, dict())
            logger.info('Created new file \'{0}\''.format(filepath))

    def save_config(self, filepath: str, data: dict) -> None:
        with open(filepath, mode='w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
