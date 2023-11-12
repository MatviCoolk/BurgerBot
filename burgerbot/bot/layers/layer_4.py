import asyncio
from typing import Callable

from telethon import Button
from telethon.errors import MessageNotModifiedError
from telethon.events import InlineQuery, CallbackQuery

from burgerbot.db import Data
from burgerbot.lang import Lang
from burgerbot.bot.layers.layer_2 import BotLayer2
from burgerbot.config import BotConfig
from burgerbot.media import Media


class BotLayer3(BotLayer2):
    def __init__(self, data: Data, media: Media, lang: Lang, bot_config: BotConfig):
        super().__init__(data=data, media=media, lang=lang, bot_config=bot_config)

        self.bot.add_event_handler(self.inline_query, InlineQuery())

    async def inline_query_handler(self, func: Callable,  event: InlineQuery.Event):
        try:
            await func(event)
        except Exception as ex:
            raise ex

    async def inline_query(self, event: InlineQuery.Event):
        sid = event.sender.id
        builder = event.builder

        self.data.inline_query_by(self.data.user(event.sender.id), event.text)

        if self.media_uploaded:
            button_data = f"v1-open-it {sid}"
            response = [
                builder.photo(self.media.open_it, buttons=[Button.inline("✅ Открыть", data=button_data)]),
                builder.photo(self.images.free_robux, buttons=[Button.inline("🤑 Получить", data=button_data)]),
                builder.photo(self.images.open_please, buttons=[Button.inline("🙂 Открыть", data=button_data)]),
                builder.photo(self.images.free_tg_prem, buttons=[Button.inline("🎁 Забрать", data=button_data)]),
                builder.photo(self.images.defend_your_account,
                              buttons=[Button.inline("ℹ️ Подробнее", data=button_data)])
            ] if event.text.lower() != "glookipail" else [
                builder.photo(self.images.glookipail, buttons=[Button.inline("💬 Написать", data=button_data)])
            ]
            await event.answer(response, gallery=True)
