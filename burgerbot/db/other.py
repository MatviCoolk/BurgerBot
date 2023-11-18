from datetime import datetime

from burgerbot.db import BaseData


class Burger:
    def __init__(self, db: BaseData, db_result: tuple, insert=False):
        self.db = db

        self.id = db_result[0]
        self.user_burgered = db_result[1]
        self.inline_query = db_result[2]
        self.datetime = datetime.strptime(db_result[1], '%Y-%m-%d %H:%M:%S') if type(db_result[3]) == str else db_result[3].replace(microsecond=0)

        if insert:
            self.db.add_to_queue(self.db.db_exec('INSERT OR IGNORE INTO burgers '
                                                 '(id, user_burgered, inline_query, datetime) VALUES (?, ?, ?, ?)',
                                                 (self.id, self.user_burgered, self.inline_query, self.datetime)))


class InlineQuery:
    def __init__(self, db: BaseData, db_result: tuple, insert=False):
        self.db = db

        self.id: int = db_result[0]
        self.sender: int = db_result[1]
        self.query: str = db_result[2]
        self.datetime: datetime = datetime.strptime(db_result[1], '%Y-%m-%d %H:%M:%S') if type(db_result[3]) == str else db_result[3].replace(microsecond=0)
        self.burger: int = 0

        if insert:
            self.db.add_to_queue(self.db.db_exec('INSERT OR IGNORE INTO inline_queries '
                                                 '(id, sender, query, datetime, burger) VALUES (?, ?, ?, ?, ?)',
                                                 (self.id, self.sender, self.query, self.datetime, self.burger)))


# class CallbackQuery:
#     def __init__(self, db, db_result: tuple):
#         self.db = db
#
#         self.id = db_result[0]
#         self.datetime = datetime.strptime(db_result[1], '%Y-%m-%d %H:%M:%S') if type(db_result[1]) == str else db_result[1]
#         self.query = db_result[2]
#         self.sender_id = db_result[3]
#
#
# class Message:
#     def __init__(self, db, db_result: tuple):
#         self.db = db
#
#         self.id = db_result[0]
#         self.message_id = db_result[1]
#         self.text = db_result[2]
#         self.datetime = datetime.strptime(db_result[3], '%Y-%m-%d %H:%M:%S') if type(db_result[3]) == str else db_result[3]
#         self.cid = db_result[4]
#         self.sender = db_result[5]
#         self.edited_to = db_result[6]
#         self.edited_of = db_result[7]
