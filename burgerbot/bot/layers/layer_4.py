import asyncio
from typing import Callable

from telethon import Button
from telethon.errors import MessageNotModifiedError
from telethon.events import InlineQuery, CallbackQuery

from burgerbot.bot.layers.layer_3 import BotLayer3
from burgerbot.db import Data
from burgerbot.lang import Lang
from burgerbot.bot.layers.layer_2 import BotLayer2
from burgerbot.config import BotConfig
from burgerbot.media import Media


class BotLayer4(BotLayer3):
    def __init__(self, data: Data, media: Media, lang: Lang, bot_config: BotConfig):
        super().__init__(data=data, media=media, lang=lang, bot_config=bot_config)

        self.bot.add_event_handler(lambda e: self.inline_query_handler(self.inline_query, e), InlineQuery())

    async def inline_query_handler(self, func: Callable,  event: InlineQuery.Event):
        try:
            await func(event)
        except Exception as ex:
            raise ex

    # THIS IS TEST
    async def inline_query(self, event: InlineQuery.Event):
        sid = event.sender.id
        builder = event.builder

        button_data = f"burger"

        response = [
            builder.photo(self.media.error, buttons=[Button.inline("test", data=button_data)]),
        ]

        await event.answer(response, gallery=True)
