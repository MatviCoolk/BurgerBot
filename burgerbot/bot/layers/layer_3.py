import asyncio

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

        self.bot.add_event_handler(lambda e: self.callback_query_handler(self.start_cq, e), CallbackQuery(pattern='start'))
        self.bot.add_event_handler(lambda e: self.callback_query_handler(self.usage_cq, e), CallbackQuery(pattern='usage'))
        self.bot.add_event_handler(lambda e: self.callback_query_handler(self.faq_cq, e), CallbackQuery(pattern='faq'))
        self.bot.add_event_handler(lambda e: self.callback_query_handler(self.more_main_cq, e), CallbackQuery(pattern='more-main'))
        self.bot.add_event_handler(lambda e: self.callback_query_handler(self.more_next_cq, e), CallbackQuery(pattern='more-next'))
        self.bot.add_event_handler(lambda e: self.callback_query_handler(self.fwd_cq, e), CallbackQuery(pattern='fwd'))
        self.bot.add_event_handler(lambda e: self.callback_query_handler(self.bug_found_cq, e), CallbackQuery(pattern='bug-found'))
        self.bot.add_event_handler(lambda e: self.callback_query_handler(self.unknown_cq, e), CallbackQuery(pattern='^(?!start|usage|faq|more|fwd|bug-found).*'))

    async def callback_query_handler(self, func, event: CallbackQuery.Event):
        if self.running:
            try:
                await func(event)
            except MessageNotModifiedError:
                pass
            except Exception as ex:
                try:
                    await event.edit(self.lang(event).error + ex.__str__(), file=self.media.error,
                                     buttons=[self.buttons.into_the_menu(event), self.buttons.report_error(event)])
                except Exception as ex1:
                    try:
                        await event.reply(self.lang(event).error + ex.__str__(),
                                          buttons=[self.buttons.into_the_menu(event), self.buttons.report_error(event)])
                    except:
                        raise ex
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
                         buttons=self.buttons.more(event, self.db.usr(event.sender.id).forward_channel_posts))

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

        if query[2] == 'more':
            await self.more_main_cq(event)

    async def unknown_cq(self, event: CallbackQuery.Event):
        await event.edit(self.lang(event).error + f"(OK) Unsupported callback query [{len(event.data)}]: b\"{str(event.data)[2:-1]}\"", file=self.media.error, link_preview=False,
                         buttons=[self.buttons.into_the_menu(event), self.buttons.report_error(event)])
