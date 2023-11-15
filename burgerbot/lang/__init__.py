import json
import sqlite3

from telethon.tl.types import User

# REQUIRED_COLUMNS = {'lang_code', 'error_occurred', 'bug_found', 'into_the_menu', 'start', 'author', 'how_to_use_btn', 'how_to_use', 'faq_btn', 'faq', 'profile', 'subscribe', 'more', 'back_to_the_menu', 'what_can_this_bot_do', 'forwarding', 'next', 'share', 'idea', 'upload_burger', 'back', 'author_btn', 'bug_found_btn', 'report', 'join_development'}
ROOT_FILLING = {'lang_code', 'error', 'bug_found', 'start', 'usage', 'faq', 'what_can_this_bot_do', 'msg_has_been_sent', 'buttons'}
BUTTONS_FILLING = {'into_the_menu', 'usage', 'back', 'author', 'faq', 'join_development', 'idea', 'upload_burger', 'bug_found', 'report', 'profile', 'subscribe', 'more', 'forwarding', 'next', 'share', 'msg_again'}
DEFAULT_LANG_CODE = 'ru'


class LanguageButtons(object):
    into_the_menu: str; usage: str; back: str; author: str; faq: str; join_development: str; idea: str;
    upload_burger: str; bug_found: str; report: str; profile: str; subscribe: str; more: str; forwarding: str;
    next: str; share: str; msg_again: str

    def __init__(self, buttons_json):
        for key in buttons_json:
            setattr(self, key, buttons_json[key])


class Language:
    lang_code: str; error: str; bug_found: str; start: str; author: str; usage: str; faq: str; msg_has_been_sent: str;
    what_can_this_bot_do: str;
    buttons: LanguageButtons

    def __init__(self, lang_json: dict):
        if set(lang_json.keys()) ^ ROOT_FILLING != set():
            raise Exception('Incorrect language file filling')

        if set(lang_json['buttons'].keys()) ^ BUTTONS_FILLING != set():
            raise Exception('Incorrect language file filling')

        self.lang_code = lang_json['lang_code']

        for key, value in lang_json.items():
            if key == 'buttons':
                self.buttons = LanguageButtons(value)
                continue
            self.__setattr__(key, value)

    def format_start(self, bot_username, sender: User) -> str:
        return self.start.replace('{BOT_USERNAME}', bot_username).replace('{MENTION}', f"<a href=\"tg://user?id={sender.id}\">{sender.first_name}</a>")


class Lang:
    def __init__(self, path: str):

        self.languages = {
            lang_code: Language(json.load(open('default_lang.json'))) for lang_code in ['ru']
        }

        self.supported_lang_codes = ['ru']

        # self.path: str = path
        #
        # # initialize sqlite3
        # self.con = sqlite3.connect(self.path)
        # self.cursor = self.con.cursor()
        #
        # columns = [lang[1] for lang in self.cursor.execute('PRAGMA table_info(languages)').fetchall()]
        #
        # if set(columns) & REQUIRED_COLUMNS != REQUIRED_COLUMNS:
        #     raise KeyError('Not enough columns in language table')
        #
        # self.supported_lang_codes = list(map(lambda t: t[0], self.cursor.execute('SELECT lang_code FROM languages').fetchall()))
        # self.languages = {
        #     row[0]: Language(row, columns) for row in self.cursor.execute('SELECT * FROM languages').fetchall()
        # }

    def __call__(self, lang_code: str) -> Language:
        if lang_code not in self.supported_lang_codes:
            lang_code = DEFAULT_LANG_CODE

        return self.languages[lang_code]
