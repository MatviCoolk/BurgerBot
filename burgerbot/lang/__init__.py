import sqlite3


COLUMNS = ['lang_code', 'error_occurred', 'bug_found', 'into_the_menu', 'start', 'author', 'how_to_use_btn', 'how_to_use', 'faq_btn', 'faq', 'profile', 'subscribe', 'more', 'back_to_the_menu', 'what_can_this_bot_do', 'forwarding', 'next', 'share', 'idea', 'upload_burger', 'back', 'author_btn', 'bug_found_btn', 'report', 'join_development']
DEFAULT_LANG_CODE = 'ru'


class Language:
    lang_code: str
    error_occurred: str
    bug_cmd: str
    into_the_menu: str
    start: str
    author: str
    how_to_use_btn: str
    how_to_use: str
    faq_btn: str
    faq: str
    profile: str
    subscribe: str
    more: str
    back_to_the_menu: str
    what_can_this_bot_do: str
    forwarding: str
    next: str
    share: str
    idea: str
    upload_burger: str
    back: str
    author_btn: str
    bug_found_btn: str
    report: str
    join_development: str

    def __init__(self, row: tuple):
        for i, column in enumerate(row):
            self.__setattr__(COLUMNS[i], column)

    def format_start(self, bot_username, sender) -> str:
        return self.start.replace('{BOT_USERNAME}', bot_username).replace('{MENTION}', f"<a href=\"tg://user?id={sender.id}\">{sender.first_name}</a>")


class Lang:
    def __init__(self, path: str):
        self.path: str = path

        # initialize sqlite3
        self.con = sqlite3.connect(self.path)
        self.cursor = self.con.cursor()

        self.supported_lang_codes = list(map(lambda t: t[0], self.cursor.execute('SELECT lang_code FROM languages').fetchall()))
        self.languages = {
            row[0]: Language(row) for row in self.cursor.execute('SELECT * FROM languages').fetchall()
        }

    def __call__(self, lang_code: str) -> Language:
        if lang_code not in self.supported_lang_codes:
            lang_code = DEFAULT_LANG_CODE

        return self.languages[lang_code]
