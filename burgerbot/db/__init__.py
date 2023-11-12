import asyncio
import sqlite3

from burgerbot.db.user import User


class Data:
    def __init__(self, path: str = 'data.db'):
        self.path: str = path

        # initialize sqlite3
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

        self.burgers, self.inline_queries, self.callback_queries = {}, {}, {}

        self.users = {}

        for db_result in self.cursor.execute("SELECT * FROM users").fetchall():
            user = User(self, db_result)
            self.users[user.tg_id] = user
            self.users[-user.id] = user


        # shorthands
        self.usr = self.user

        asyncio.ensure_future(self.auto_commit())

    def save(self):
        for user in self.users.values():
            user.update()
        self.connection.commit()

    async def auto_commit(self):
        while True:
            await asyncio.sleep(60 * 5)
            self.save()

    def save_and_close(self):
        self.save()
        self.cursor.execute('VACUUM')
        self.connection.close()

    def user(self, user_id: int) -> User:
        if user_id in self.users.keys():
            return self.users[user_id]

        db_result = self.cursor.execute(f"SELECT * FROM users WHERE id = \'{user_id}\'").fetchone()
        if db_result is None:
            user = User(self, (user_id,)).update()
        else:
            user = User(self, db_result)

        self.users[user_id] = user
        return user
