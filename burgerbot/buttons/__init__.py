from typing import Union, Callable

from telethon import Button
from telethon.events import NewMessage, CallbackQuery, InlineQuery

from burgerbot.lang import Lang, Language


class Buttons:
    def __init__(self, lang: Callable[[Union[None, str, int, NewMessage.Event, CallbackQuery.Event, InlineQuery.Event]], Language]):
        self.lang = lang

    def start(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        return [
            [Button.inline('🍔 ' + self.lang(event).how_to_use_btn, 'usage')],
            [Button.inline('📸 ' + self.lang(event).profile, 'profile'),
             Button.url('❤️ ' + self.lang(event).subscribe, 'https://t.me/+AIzgI1gejr45NDJi')],
            [Button.inline('✳️ ' + self.lang(event).faq_btn, 'faq'),
             Button.inline('💠 ' + self.lang(event).more, 'more-main')]
        ]

    def author_cmd(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        return [
            Button.inline('◀️ ' + self.lang(event).into_the_menu, 'start author_cmd')
        ]

    def into_the_menu(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        return Button.inline('◀️ ' + self.lang(event).into_the_menu, 'start')

    def back_to_the_menu(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        return Button.inline('◀️ ' + self.lang(event).back_to_the_menu, 'start')

    def back(self, event: Union[NewMessage.Event, CallbackQuery.Event], dest='start'):
        return Button.inline('◀️ ' + self.lang(event).back_to_the_menu, dest)

    def report_error(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        return Button.url('💘 ' + self.lang(event).report, 't.me/matvicoolk1')

    def more(self, event: Union[NewMessage.Event, CallbackQuery.Event], fwd: bool):
        lang = self.lang(event)

        return [[Button.inline('🖼️ ' + lang.upload_burger, 'upload-burger')],
                [Button.inline(('🔔 ' if fwd else '🔕 ') + lang.forwarding, 'fwd ' + ('off' if fwd else 'on') + ' more'),
                 Button.switch_inline('💌' + lang.share, '')],
                [Button.inline('💭 ' + lang.idea, 'idea')],
                [self.back_to_the_menu(event),
                 Button.inline('▶️ ' + lang.next, 'more-next')]]

    def more_next(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        lang = self.lang(event)

        return [
            [Button.inline('💠 ' + lang.author_btn, 'author'),
             Button.url('🧰 GitHub', "https://github.com/MatviCoolk/BurgerBot")],
            [Button.inline('🤨 ' + lang.join_development, 'join-dev')],
            [self.back(event, 'more-main'),
             Button.inline('⚠️ ' + lang.bug_found_btn, 'bug-found more-next')]
        ]
