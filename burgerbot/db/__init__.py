import asyncio

from burgerbot.db.base import BaseData
from burgerbot.db.user import User


class Data(BaseData):
    def __init__(self, path: str = 'data.db'):
        super().__init__(path)

        asyncio.get_event_loop().run_until_complete(self._async_init())

    async def _async_init(self):
        await super()._async_init()

        for db_result in await self.db_exec_fetchall("SELECT * FROM users"):
            user = User(self, db_result)
            self.users[user.tg_id] = user
            self.users[-user.id] = user

    async def _get_user(self, user_id: int) -> User:
        if user_id in self.users.keys():
            return self.users[user_id]

        db_result = await self.db_exec_fetchone(f"SELECT * FROM users WHERE telegram_id = \'{user_id}\'")

        if db_result is not None:
            usr = User(self, db_result)
        else:
            usr = User(self, (user_id,))

        self.users[user_id] = usr
        return usr

    def usr(self, user_id: int) -> User:
        future = asyncio.Future()
        self.add_to_queue(self._get_user(user_id), future)
        return asyncio.get_event_loop().run_until_complete(future)