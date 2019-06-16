from discord.ext import commands

import traceback


INITIAL_EXTENSIONS = ()


class GSBot(commands.Bot):
    def __init__(self):
        super().__init__()

        for ext in INITIAL_EXTENSIONS:
            try:
                self.load_extension(ext)
            except Exception:
                traceback.print_exc()
