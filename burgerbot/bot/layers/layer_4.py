import asyncio
from typing import Callable

from telethon import Button
from telethon.errors import MessageNotModifiedError
from telethon.events import InlineQuery, CallbackQuery

from burgerbot.bot.layers.layer_3 import BotLayer3
from burgerbot.buttons import CQ_PREFIX
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

        iq_id = self.db.inline_query_by(sid, event.text).id

        usr = self.db.usr(sid)

        # if usr.blocked or not usr.dialog_started:
        #     await event.answer([], gallery=True, cache_time=20, switch_pm='/start — Запустить бота',
        #                        switch_pm_param='iq_start', private=True)

        button_data = f"{CQ_PREFIX}burger {iq_id}"

        response = [
            builder.photo(self.media.error, buttons=[Button.inline("test", data=button_data)]),
        ]

        await event.answer(response, gallery=True, cache_time=0, switch_pm='Начать использовать', switch_pm_param='l', private=True)
