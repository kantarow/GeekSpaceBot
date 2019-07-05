from discord.ext import commands

import traceback
import json
import logging


INITIAL_EXTENSIONS = ('extensions.genembed', 'extensions.vcrole', 'extensions.gnupdate')
logger = logging.getLogger('gsbot')


class GSBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='g!')

        self.config = self.load_config('config/config.json')

        for ext in INITIAL_EXTENSIONS:
            try:
                self.load_extension(ext)
            except Exception:
                traceback.print_exc()

    async def start(self):
        await super().start(self.config['Token'])

    def load_config(self, filepath: str, *, default=None) -> dict:
        """
        configファイルを読み込みます。
        もしファイルが存在しない場合は自動で空のファイルを生成します。
        生成するファイルを殻にしたくない場合はdefaultにdict型のオブジェクトを渡してください。
        """
        try:
            with open(filepath, mode='r', encoding='utf8') as f:
                return json.load(f)
        except OSError:
            logger.error('Configuration file is not found.')
            self.save_config(filepath, dict() if default is None else default)
            logger.info('Created new file \'{0}\''.format(filepath))

    def save_config(self, filepath: str, data: dict) -> None:
        with open(filepath, mode='w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
