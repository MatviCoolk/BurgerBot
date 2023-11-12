from telethon import Button
from telethon.events import NewMessage

from burgerbot.db import Data
from burgerbot.bot.layers.layer_1 import BotLayer1
from burgerbot.config import BotConfig
from burgerbot.lang import Lang
from burgerbot.media import Media


class BotLayer2(BotLayer1):
    def __init__(self, data: Data, media: Media, lang: Lang, bot_config: BotConfig):
        super().__init__(data=data, media=media, lang=lang, bot_config=bot_config)

        self.bot.add_event_handler(lambda e: self.new_message_handler(self.start_cmd, e), NewMessage(pattern='/start'))
        self.bot.add_event_handler(lambda e: self.new_message_handler(self.bug_cmd, e), NewMessage(pattern='/bug'))
        self.bot.add_event_handler(lambda e: self.new_message_handler(self.author_cmd, e), NewMessage(pattern='/author'))
        self.bot.add_event_handler(lambda e: self.new_message_handler(self.usage_cmd, e), NewMessage(pattern='/usage'))
        self.bot.add_event_handler(lambda e: self.new_message_handler(self.any_msg, e), NewMessage())

    async def new_message_handler(self, func, event: NewMessage.Event):
        if self.running:
            try:
                await func(event)
            except Exception as ex:
                await event.reply(self.lang(event).error_occurred)
                raise ex

    async def any_msg(self, event: NewMessage.Event):
        print(event)

    async def start_cmd(self, event: NewMessage.Event):
        await event.respond(self.lang(event).format_start(self.username, event.sender), file=self.media.burger_bot,
                            buttons=self.buttons.start(event))

    async def bug_cmd(self, event: NewMessage.Event):
        await event.respond(self.lang(event).bug_found, file=self.media.bug_found,
                            buttons=[self.buttons.into_the_menu(event)])

    async def author_cmd(self, event: NewMessage.Event):
        await event.respond(self.lang(event).author, file=self.media.under_construction,
                            buttons=self.buttons.author_cmd(event))

    async def usage_cmd(self, event: NewMessage.Event):
        await event.respond(self.lang(event).how_to_use, file=self.media.usage,
                            buttons=[self.buttons.into_the_menu(event)])
