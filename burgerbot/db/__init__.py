import asyncio
import datetime

from burgerbot.db.base import BaseData
from burgerbot.db.other import Burger, InlineQuery
from burgerbot.db.user import User


def missing_id(ids: set):
    return list(set(range(max(list(ids | {0})) + 1)).difference(ids))[0]


class Data(BaseData):
    def __init__(self, path: str = 'data.db'):
        super().__init__(path)

        asyncio.get_event_loop().run_until_complete(self.async_init())

    async def async_init(self):
        await super().async_init()

        for db_result in await self.db_exec_fetchall('SELECT * FROM users'):
            user = User(self, db_result)
            self.users[user.id] = user

    async def _get_user(self, user_id: int) -> User:
        if user_id in self.users.keys():
            return self.users[user_id]

        db_result = await self.db_exec_fetchone(f"SELECT * FROM users WHERE id = \'{user_id}\'")

        if db_result is not None:
            usr = User(self, db_result)
        else:
            usr = User(self, (user_id,))

        self.users[user_id] = usr
        return usr

    async def _get_burger(self, burger_id: int) -> Burger:
        if burger_id in self.burgers.keys():
            return self.burgers[burger_id]

        db_result = await self.db_exec_fetchone(f"SELECT * FROM burgers WHERE id = \'{burger_id}\'")

        if db_result is not None:
            return Burger(self, db_result)
        else:
            raise KeyError('Burger with provided ID does not exist')

    async def _get_iq(self, iq_id: int) -> InlineQuery:
        if iq_id in self.inline_queries.keys():
            return self.inline_queries[iq_id]

        db_result = await self.db_exec_fetchone(f"SELECT * FROM inline_queries WHERE id = \'{iq_id}\'")

        if db_result is not None:
            return InlineQuery(self, db_result)
        else:
            raise KeyError('Inline query with passed ID does not exist')

    def inline_query_by(self, user_id: int, query: str) -> InlineQuery:
        iq_id = missing_id(set(self.inline_queries.keys()))

        iq = InlineQuery(self, (iq_id, user_id, query, datetime.datetime.now(), None), insert=True)
        self.inline_queries[iq_id] = iq_id
        return iq

    def burger(self, user_id: int, inline_query_id: int) -> Burger:
        burger_id = missing_id(set(self.burgers.keys()))

        burger = Burger(self, (burger_id, user_id, inline_query_id, datetime.datetime.now()), insert=True)
        self.burgers[burger_id] = burger
        return burger

    def get_inline_query(self, iq_id):
        future = asyncio.Future()
        self.add_to_queue(self._get_iq(iq_id), future)
        return asyncio.run(asyncio.wait_for(future, None))

    def get_burger(self, burger_id: int) -> User:
        future = asyncio.Future()
        self.add_to_queue(self._get_burger(burger_id), future)
        return asyncio.run(asyncio.wait_for(future, None))

    def usr(self, user_id: int) -> User:
        future = asyncio.Future()
        self.add_to_queue(self._get_user(user_id), future)
        return asyncio.run(asyncio.wait_for(future, None))
