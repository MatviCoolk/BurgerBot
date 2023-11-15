from typing import Union, Callable

from telethon import Button
from telethon.events import NewMessage, CallbackQuery, InlineQuery

from burgerbot.lang import Lang, Language


class Buttons:
    def __init__(self, lang: Callable[[Union[None, str, int, NewMessage.Event, CallbackQuery.Event, InlineQuery.Event]], Language]):
        self.lang = lang

    def start(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        lang_buttons = self.lang(event).buttons
        return [
            [Button.inline('🍔 ' + lang_buttons.usage, 'usage')],
            [Button.inline('📸 ' + lang_buttons.profile, 'profile'),
             Button.url('❤️ ' + lang_buttons.subscribe, 'https://t.me/+AIzgI1gejr45NDJi')],
            [Button.inline('✳️ ' + lang_buttons.faq, 'faq'),
             Button.inline('💠 ' + lang_buttons.more, 'more-main')]
        ]

    def author_cmd(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        return [
            Button.inline('◀️ ' + self.lang(event).buttons.into_the_menu, 'start author_cmd')
        ]

    def into_the_menu(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        return Button.inline('◀️ ' + self.lang(event).buttons.into_the_menu, 'start')

    def back_to_the_menu(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        return Button.inline('◀️ ' + self.lang(event).buttons.back, 'start')

    def back(self, event: Union[NewMessage.Event, CallbackQuery.Event], dest='start'):
        return Button.inline('◀️ ' + self.lang(event).buttons.back, dest)

    def report_error(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        return Button.url('💘 ' + self.lang(event).buttons.report, 't.me/matvicoolk1')

    def more(self, event: Union[NewMessage.Event, CallbackQuery.Event], fwd: bool):
        lang_buttons = self.lang(event).buttons

        return [[Button.inline('🖼️ ' + lang_buttons.upload_burger, 'upload-burger')],
                [Button.inline(('🔔 ' if fwd else '🔕 ') + lang_buttons.forwarding, 'fwd ' + ('off' if fwd else 'on') + ' more'),
                 Button.switch_inline('💌' + lang_buttons.share, '')],
                [Button.inline('💭 ' + lang_buttons.idea, 'idea')],
                [self.back_to_the_menu(event),
                 Button.inline('▶️ ' + lang_buttons.next, 'more-next')]]

    def more_next(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        lang_buttons = self.lang(event).buttons

        return [
            [Button.inline('💠 ' + lang_buttons.author, 'author'),
             Button.url('🧰 GitHub', "https://github.com/MatviCoolk/BurgerBot")],
            [Button.inline('🐍 ' + lang_buttons.join_development, 'join-dev')],
            [self.back(event, 'more-main'),
             Button.inline('⚠️ ' + lang_buttons.bug_found, 'bug-found more-next')]
        ]
