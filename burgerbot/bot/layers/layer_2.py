from telethon import Button
from telethon.events import NewMessage
from telethon.tl.types import User, MessageMediaDocument, MessageMediaPhoto, MessageMediaContact, MessageMediaEmpty, MessageMediaPoll

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
        self.bot.add_event_handler(lambda e: self.new_message_handler(self.non_cmd_msg, e), NewMessage(pattern='^(?!/start|/bug|/author|/usage).*'))

    async def new_message_handler(self, func, event: NewMessage.Event):
        if self.running:
            try:
                await func(event)
            except Exception as ex:
                await event.reply(self.lang(event).error + str(ex), buttons=[self.buttons.report_error(event)])
                raise ex

    async def non_cmd_msg(self, event: NewMessage.Event):
        if type(event.chat) != User:
            return

        await event.respond('self.lang(event).msg_has_been_sent', buttons=[self.buttons.send_another_msg(event)])

    async def any_msg(self, event: NewMessage.Event):
        try:
            await event.respond(event.message.message, file=event.message.media)
        except:
            await event.forward_to(event.chat)

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
        await event.respond(self.lang(event).usage, file=self.media.usage,
                            buttons=[self.buttons.into_the_menu(event)])
