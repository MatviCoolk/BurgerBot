from typing import Union, Callable

from telethon import Button
from telethon.events import NewMessage, CallbackQuery, InlineQuery

from burgerbot.lang import Lang, Language


CQ_PREFIX = 'v3-'


def inline(text: str, data: str):
    return Button.inline(text, CQ_PREFIX + data)


class Buttons:
    def __init__(self, lang: Callable[[Union[None, str, int, NewMessage.Event, CallbackQuery.Event, InlineQuery.Event]], Language]):
        self.lang = lang

    def start(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        lang_buttons = self.lang(event).buttons
        return [
            [inline('🍔 ' + lang_buttons.usage, 'usage')],
            [inline('📸 ' + lang_buttons.profile, 'profile'),
             Button.url('❤️ ' + lang_buttons.subscribe, 'https://t.me/+AIzgI1gejr45NDJi')],
            [inline('✳️ ' + lang_buttons.faq, 'faq'),
             inline('💠 ' + lang_buttons.more, 'more-main')]
        ]

    def author_cmd(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        return [
            inline('◀️ ' + self.lang(event).buttons.into_the_menu, 'start author_cmd')
        ]

    def into_the_menu(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        return inline('◀️ ' + self.lang(event).buttons.into_the_menu, 'start')

    def back_to_the_menu(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        return inline('◀️ ' + self.lang(event).buttons.back, 'start')

    def back(self, event: Union[NewMessage.Event, CallbackQuery.Event], dest='start'):
        return inline('◀️ ' + self.lang(event).buttons.back, dest)

    def report_error(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        return Button.url('💘 ' + self.lang(event).buttons.report, 't.me/matvicoolk1')

    def more_main(self, event: Union[NewMessage.Event, CallbackQuery.Event], fwd: bool):
        lang_buttons = self.lang(event).buttons
        print('l')

        return [[inline('🖼️ ' + lang_buttons.upload_burger, 'upload-burger')],
                [inline(('🔔 ' if fwd else '🔕 ') + lang_buttons.forwarding, 'fwd ' + ('off' if fwd else 'on') + ' more-main'),
                 Button.switch_inline('💌' + lang_buttons.share, '')],
                [inline('💭 ' + lang_buttons.idea, 'idea')],
                [self.back_to_the_menu(event),
                 inline('▶️ ' + lang_buttons.next, 'more-next')]]

    def more_next(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        lang_buttons = self.lang(event).buttons

        return [
            [inline('💠 ' + lang_buttons.author, 'author'),
             Button.url('🧰 GitHub', "https://github.com/MatviCoolk/BurgerBot")],
            [inline('🐍 ' + lang_buttons.join_development, 'join-dev')],
            [self.back(event, 'more-main'),
             inline('⚠️ ' + lang_buttons.bug_found, 'bug-found more-next')]
        ]

    def send_another_msg(self, event: Union[NewMessage.Event, CallbackQuery.Event]):
        lang_buttons = self.lang(event).buttons

        return [
            inline('💬 ' + 'lang_buttons.send_another_msg', 'send-another-msg')
        ]
