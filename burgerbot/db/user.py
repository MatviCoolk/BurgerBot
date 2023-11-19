from datetime import datetime
from sqlite3 import Row
from typing import Self, Union

from burgerbot.db import BaseData
from burgerbot.db.encoding_list import decode, encode


class User:
    def __init__(self, db: BaseData, db_result: Union[Row, tuple]):
        if len(db_result) < 1:
            raise ValueError('User ID not specified')
        elif len(db_result) == 1:
            db_result = (db_result[0], 0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0, 2, '', '', '', '', '', 0, '', 'ru')

        self.id = db_result[0]

        # info & settings
        self.dialog_started = bool(db_result[2] % 2)
        self.blocked = bool((db_result[2] >> 1) % 2)

        self.show_about_in_start_msg = bool(db_result[3] % 2)
        self.forward_channel_posts = bool((db_result[3] >> 1) % 2)

        # events
        self.burger_ids = decode(db_result[4])
        self.inline_query_ids = decode(db_result[5])
        self.callback_query_ids = decode(db_result[6])
        self.message_ids = decode(db_result[7])

        # other info
        self.join_date = datetime.strptime(db_result[1], '%Y-%m-%d %H:%M:%S')
        self.reputation = db_result[8]
        self.md_link = db_result[9]
        self.lang_code = db_result[10]

        self.db = db

    # def burgered_by(self, user_id: int):
    #     self.db.burger(self, self.db.user(user_id))
    #
    # def callback_query(self, query: bytes):
    #     self.db.callback_query_by(self, query)
    #
    # def new_message(self, cid, text, msg_id):
    #     self.db.new_message(self, cid, text, msg_id)

    @property
    def info(self):
        return int(self.dialog_started) + int(self.blocked) * 2

    @property
    def settings(self):
        return int(self.show_about_in_start_msg) + int(self.forward_channel_posts) * 2

    @property
    def was_burgered(self):
        return [burger for burger in self.burger_ids if self.db.get_burger(burger).user_burgered == self.id]

    async def update(self) -> Self:
        await self.db.db_exec('INSERT OR REPLACE INTO users (id, join_date, info, settings, burgers, inline_queries, callback_queries, messages, reputation, md_link, lang_code) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                              (self.id, self.join_date, self.info, self.settings, encode(self.burger_ids), encode(self.inline_query_ids), encode(self.callback_query_ids), encode(self.message_ids), self.reputation, self.md_link, self.lang_code))

        return self
