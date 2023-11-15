import asyncio
import aiosqlite
from aiosqlite import Cursor, Connection
from collections import deque


class BaseData:
    connection: Connection
    cursor: Cursor

    def __init__(self, path: str = 'data.db'):
        self.path: str = path

        self.burgers, self.inline_queries, self.callback_queries = {}, {}, {}

        self.users = {}

        self._queue_processing_event = asyncio.Event()
        self.deque = deque()

        asyncio.ensure_future(self._process_queue())

    async def _async_init(self):
        # initialize sqlite3
        self.connection = await aiosqlite.connect(self.path)
        self.cursor = await self.connection.cursor()

        asyncio.ensure_future(self._auto_commit())

    async def _process_queue(self):
        while True:
            if not self.deque:
                self._queue_processing_event.clear()
                await self._queue_processing_event.wait()

            request: asyncio.coroutine; future: asyncio.Future

            request, future = self.deque.popleft()
            result = await request
            if future is not None:
                future.set_result(result)

    def add_to_queue(self, coroutine, future=None):
        self.deque.append((coroutine, future))
        self._queue_processing_event.set()

    # SHORTHANDS
    async def db_exec(self, sql: str, parameters=()) -> aiosqlite.Cursor:
        if parameters == ():
            return await self.cursor.execute(sql)
        return await self.cursor.execute(sql, parameters)

    async def db_exec_fetchall(self, sql: str, parameters=()):
        await self.db_exec(sql, parameters)
        return await self.db_fetchall()

    async def db_exec_fetchone(self, sql: str, parameters=()):
        await self.db_exec(sql, parameters)
        return await self.db_fetchone()

    async def db_fetchall(self):
        return await self.cursor.fetchall()

    async def db_fetchone(self):
        return await self.cursor.fetchone()

    async def _save(self):
        tasks = []

        for user in self.users.values():
            tasks.append(asyncio.create_task(user.update()))
        for task in tasks:
            await task

        await self.connection.commit()

    def save(self):
        self.add_to_queue(self._save())

    async def _auto_commit(self):
        while True:
            await asyncio.sleep(60 * 5)
            self.save()

    async def save_and_close(self):
        self.save()
        self.add_to_queue(self.db_exec('VACUUM'))
        await self.connection.close()
