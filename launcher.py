import contextlib
import logging
import asyncio

from logging.handlers import RotatingFileHandler
from gsbot import GSBot


@contextlib.contextmanager
def setup_logger():
    try:
        bot_logger = logging.getLogger('gsbot')
        bot_logger.setLevel(logging.WARNING)
        discord_logger = logging.getLogger('discord')
        discord_logger.setLevel(logging.WARNING)

        bot_handler = RotatingFileHandler(
            filename='gsbot.log',
            maxBytes=1048576,
            backupCount=4
        )
        discord_handler = RotatingFileHandler(
            filename='discord.log',
            maxBytes=1048576,
            backupCount=4
        )

        fmt = logging.Formatter(
            '[{asctime}][{levelname}] {name}: {message}',
            '%Y-%m-%d %H:%M:%S',
            style='{'
        )

        bot_handler.setFormatter(fmt)
        discord_handler.setFormatter(fmt)

        bot_logger.addHandler(bot_handler)
        discord_logger.addHandler(discord_logger)

    finally:
        handlers = bot_handler[:]

        for h in handlers:
            h.close()
            bot_logger.removeHandler(h)

        handlers = discord_handler[:]

        for h in handlers:
            h.close()
            discord_logger.removeHandler(h)


async def setup_database():
    pass


async def run_bot():
    with setup_logger():
        bot = GSBot()
        await bot.start()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
    loop.close()


if __name__ == '__main__':
    main()
