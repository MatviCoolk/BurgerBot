import asyncio
import aiosqlite
from aiosqlite import Cursor, Connection
from collections import deque


class BaseData:
    connection: Connection
    cursor: Cursor

    def __init__(self, path: str = 'data.db'):
        self.path: str = path

        self.users, self.burgers, self.inline_queries, self.callback_queries = {}, {}, {}, {}

        self._queue_processing_event = asyncio.Event()
        self.deque = deque()

        asyncio.ensure_future(self.process_queue())

    async def async_init(self):
        # initialize sqlite3
        self.connection = await aiosqlite.connect(self.path)
        self.cursor = await self.connection.cursor()

        await self.db_exec('CREATE TABLE IF NOT EXISTS "users" ('
                           '"id" INT NOT NULL,'
                           '"join_date" datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, '
                           '"info" INT NOT NULL DEFAULT \'0\', '
                           '"settings" INT NOT NULL DEFAULT \'0\', '
                           '"burgers" BLOB NOT NULL DEFAULT \'\', '
                           '"inline_queries" BLOB NOT NULL DEFAULT \'\', '
                           '"callback_queries" BLOB NOT NULL DEFAULT \'\', '
                           '"messages" BLOB NOT NULL DEFAULT \'\', '
                           '"reputation" INT NOT NULL DEFAULT \'0\', '
                           '"md_link" TEXT NOT NULL DEFAULT \'\', '
                           '"lang_code" TEXT NOT NULL DEFAULT \'ru\', '
                           'PRIMARY KEY (id));')

        await self.db_exec('CREATE TABLE IF NOT EXISTS "inline_queries" ('
                           '"id" int NOT NULL,'
                           '"sender" int NOT NULL,'
                           '"query" text NOT NULL DEFAULT \'\', '
                           '"datetime" datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, '
                           '"burger" INT, '
                           'PRIMARY KEY (id))')

        await self.db_exec('CREATE TABLE IF NOT EXISTS "burgers" ('
                           '"id" int NOT NULL, '
                           '"user_burgered" int NOT NULL, '
                           '"inline_query" int NOT NULL, '
                           '"datetime" datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, '
                           'PRIMARY KEY (id));')

        asyncio.ensure_future(self.auto_commit())

    async def process_queue(self):
        while True:
            if not self.deque:
                self._queue_processing_event.clear()
                await self._queue_processing_event.wait()

            request: asyncio.coroutine; future: asyncio.Future

            request, future = self.deque.popleft()
            print(request)
            result = await request
            if future is not None:
                print('result')
                future.set_result(result)

    def add_to_queue(self, coroutine, future=None):
        self.deque.append((coroutine, future))
        self._queue_processing_event.set()

    # SHORTHANDS
    async def db_exec(self, sql: str, parameters=()) -> aiosqlite.Cursor:
        print(sql)
        if parameters == ():
            return await self.cursor.execute(sql)
        return await self.cursor.execute(sql, parameters)

    async def db_exec_fetchall(self, sql: str, parameters=()):
        await self.db_exec(sql, parameters)
        return await self.db_fetchall()

    async def db_exec_fetchone(self, sql: str, parameters=()):
        await self.db_exec(sql, parameters)
        print('e')
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

    async def auto_commit(self):
        while True:
            await asyncio.sleep(60 * 5)
            self.save()

    async def save_and_close(self):
        self.save()
        self.add_to_queue(self.db_exec('VACUUM'))

        future = asyncio.Future()
        self.add_to_queue(self.connection.close(), future)
        await future
