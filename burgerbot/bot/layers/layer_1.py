import asyncio
import json
from typing import Union

from telethon import TelegramClient
from telethon.events import NewMessage, InlineQuery, CallbackQuery
from telethon.tl.types import Message, User

from burgerbot.buttons import Buttons
from burgerbot.config import BotConfig
from burgerbot.db import Data
from burgerbot.media import Media, BotMedia
from burgerbot.lang import Lang, DEFAULT_LANG_CODE


class BotLayer1:
    def __init__(self, data: Data, media: Media, lang: Lang, bot_config: BotConfig):
        self.me: User = ...
        self.username: str = ...
        self.id: int = ...

        self.db: Data = data
        self.media_full = media
        self.config = bot_config
        self.media: BotMedia = ...

        self.__lang = lang
        self.buttons = Buttons(self.lang)
        # self.lang — shorthand to Lang()

        # markdown doesn't have underlining >:O
        self.bot = TelegramClient(self.config.session, self.config.app_id, self.config.app_hash)
        self.bot.parse_mode = 'html'
        self.bot.start(bot_token=self.config.token)

        # status
        self.running = False
        self.media_uploaded = False

        asyncio.ensure_future(self.async_init())

    async def async_init(self):
        self.me = await self.bot.get_me()
        self.username = self.me.username
        self.id = self.me.id

        with open(self.config.necessary_media, 'r') as necessary_media_file:
            self.media = await self.media_full.bot(json.load(necessary_media_file), self.bot, self.id)

        self.running = True

    def stop(self):
        self.running = False
        self.bot.disconnect()

    # =================================================== SHORTHANDS ===================================================

    async def msg(self, entity, message, buttons=None, file=None, link_preview=False, reply_to=None) -> Message:
        return await self.bot.send_message(entity=entity, message=message, buttons=buttons, file=file, link_preview=link_preview, reply_to=reply_to)

    def lang(self, lang_code: Union[None, str, int, NewMessage.Event, InlineQuery.Event, CallbackQuery.Event]):
        match lang_code:
            case None:
                return self.__lang(DEFAULT_LANG_CODE)
            case str():
                return self.__lang(lang_code)
            case int():
                return self.__lang(self.db.usr(lang_code).lang_code)
            case NewMessage.Event(), InlineQuery.Event(), CallbackQuery.Event():
                return self.__lang(self.db.usr(lang_code.sender.id).lang_code)
            case _:
                return self.__lang(DEFAULT_LANG_CODE)
