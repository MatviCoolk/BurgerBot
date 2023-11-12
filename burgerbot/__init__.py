import os
import signal
from typing import List
from setproctitle import setproctitle
from telethon import TelegramClient

from burgerbot.bot import Bot
from burgerbot.config import Config
from burgerbot.db import Data
from burgerbot.lang import Lang
from burgerbot.media import Media

PROCESS_TITLE = 'BURGER-BOT'


def run(path_to_config_file):
    setproctitle(PROCESS_TITLE)

    config = Config(path_to_config_file)
    bots = []

    logging = {}
    lang = {}
    media = {}
    data = {}

    def on_sigint(*args):
        for bot in bots:
            bot.stop()

        for data_sing in data.values():
            data_sing.save_and_close()

        exit()

    signal.signal(signal.SIGINT, on_sigint)

    for bot_config in config.bots:
        if bot_config.testing == config.testing:
            if bot_config.db_path not in data.keys():
                data[bot_config.db_path] = Data(bot_config.db_path)

            if bot_config.lang_config_path not in lang.keys():
                lang[bot_config.lang_config_path] = Lang(bot_config.lang_config_path)

            if bot_config.media not in media.keys():
                media[bot_config.media] = Media(bot_config.media)

            bots.append(Bot(data[bot_config.db_path], media[bot_config.media], lang[bot_config.lang_config_path], bot_config))

    for bot in bots:
        bot.bot.run_until_disconnected()
        bot.stop()

    for data_sing in data.values():
        data_sing.save_and_close()
