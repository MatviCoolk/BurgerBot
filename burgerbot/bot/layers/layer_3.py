import asyncio
from typing import Callable

from telethon.errors import MessageNotModifiedError
from telethon.events import InlineQuery, CallbackQuery

from burgerbot.buttons import CQ_PREFIX
from burgerbot.db import Data
from burgerbot.lang import Lang
from burgerbot.bot.layers.layer_2 import BotLayer2
from burgerbot.config import BotConfig
from burgerbot.media import Media


class BotLayer3(BotLayer2):
    def __init__(self, data: Data, media: Media, lang: Lang, bot_config: BotConfig):
        super().__init__(data=data, media=media, lang=lang, bot_config=bot_config)

        self.add_cq_event_handler(self.start_cq, 'start')
        self.add_cq_event_handler(self.usage_cq, 'usage')
        self.add_cq_event_handler(self.faq_cq, 'faq')
        self.add_cq_event_handler(self.more_main_cq, 'more-main')
        self.add_cq_event_handler(self.more_next_cq, 'more-next')
        self.add_cq_event_handler(self.fwd_cq, 'fwd')
        self.add_cq_event_handler(self.bug_found_cq, 'bug-found')
        self.add_cq_event_handler(self.burger_cq, 'burger')
        self.add_cq_event_handler(self.unknown_cq, f"^(?!{CQ_PREFIX}(start|usage|faq|more|fwd|bug-found|burger)).*", add_prefix=False)

    def add_cq_event_handler(self, func, data, add_prefix=True):
        pattern = CQ_PREFIX + data if add_prefix else data
        self.bot.add_event_handler(lambda e: self.callback_query_handler(func, e), CallbackQuery(pattern=pattern))

    async def callback_query_handler(self, func, event: CallbackQuery.Event):
        print(event)
        if self.running:
            try:
                await func(event)
            except MessageNotModifiedError:
                pass
            except Exception as ex:
                try:
                    await event.edit(self.lang(event).error + str(ex), file=self.media.error,
                                     buttons=[self.buttons.into_the_menu(event), self.buttons.report_error(event)])
                except any:
                    pass
                raise ex

    async def start_cq(self, event: CallbackQuery.Event):
        sid = event.sender.id
        await event.edit(self.lang(sid).format_start(self.username, event.sender), file=self.media.burger_bot, link_preview=False,
                         buttons=self.buttons.start(event))

    async def usage_cq(self, event: CallbackQuery.Event):
        sid = event.sender.id
        await event.edit(self.lang(sid).usage, file=self.media.usage, link_preview=False,
                         buttons=[self.buttons.back(event)])

    async def faq_cq(self, event: CallbackQuery.Event):
        await event.edit(self.lang(event).faq, file=self.media.faq, link_preview=False,
                         buttons=[self.buttons.back(event)])

    async def more_main_cq(self, event: CallbackQuery.Event):
        await event.edit(self.lang(event).what_can_this_bot_do, file=self.media.more, link_preview=False,
                         buttons=self.buttons.more_main(event, self.db.usr(event.sender.id).forward_channel_posts))

    async def more_next_cq(self, event: CallbackQuery.Event):
        await event.edit('', file=self.media.under_construction, link_preview=False,
                         buttons=self.buttons.more_next(event))

    async def bug_found_cq(self, event: CallbackQuery.Event):
        data = event.data.decode().split()
        await event.edit(self.lang(event).bug_found, file=self.media.bug_found,
                         buttons=[self.buttons.back(event, ' '.join(data[1:]))])

    async def fwd_cq(self, event: CallbackQuery.Event):
        query = event.data.decode().split()
        self.db.usr(event.sender.id).forward_channel_posts = query[1] == 'on'

        if len(query) < 3:
            return

        if query[2].remove_prefix(CQ_PREFIX) == 'more-main':
            await self.more_main_cq(event)

    async def burger_cq(self, event: CallbackQuery.Event):
        await event.edit(self.lang(event).just_got_burgered(event.sender, self.db), link_preview=False,
                         file=self.media.you_just_got_burgered)

    async def unknown_cq(self, event: CallbackQuery.Event):
        await event.edit(self.lang(event).error + f"(OK) Unsupported callback query [{len(event.data)}]: b\"{str(event.data)[2:-1]}\"", file=self.media.error, link_preview=False,
                         buttons=[self.buttons.into_the_menu(event), self.buttons.report_error(event)])
