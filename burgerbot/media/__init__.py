import datetime
import sqlite3
from typing import Dict, Union

from telethon import TelegramClient
from telethon.tl.functions.messages import UploadMediaRequest
from telethon.tl.types import MessageMediaPhoto, Photo, MessageMediaDocument, InputPeerSelf, InputMediaUploadedPhoto, InputMediaUploadedDocument, Document


PARENT_FOLDER_KEY = 'parent_folder'
GIFS_KEY = 'gifs'
NECESSARY_TABLE = 'necessary_bot'
UPLOADS_TABLE = 'uploads_bot'


class BotMedia:
    REQUIRED_NECESSARY_MEDIA = {'under_construction', 'burger_bot', 'bug_found', 'error', 'usage', 'faq', 'more', 'you_just_got_burgered'}

    under_construction: MessageMediaPhoto
    burger_bot: MessageMediaPhoto
    bug_found: MessageMediaPhoto
    error: MessageMediaPhoto
    usage: MessageMediaDocument
    faq: MessageMediaPhoto
    more: MessageMediaPhoto
    you_just_got_burgered: MessageMediaPhoto

    def __init__(self, necessary: Dict[str, Union[MessageMediaPhoto, MessageMediaDocument]]):
        # if set(necessary.keys()) & self.REQUIRED_NECESSARY_MEDIA != self.REQUIRED_NECESSARY_MEDIA:
        #     raise KeyError('Some necessary media missing while initializing BotMedia')  # won't happen... maybe

        for name, media in necessary.items():
            self.__setattr__(name, media)


async def upload_media(client: TelegramClient, path: str, gif: bool = False) -> Union[MessageMediaPhoto, MessageMediaDocument]:
    file = await client.upload_file(path)

    if gif:
        media = InputMediaUploadedDocument(file, mime_type='video/mp4', attributes=[])
    else:
        media = InputMediaUploadedPhoto(file)

    return await client(UploadMediaRequest(InputPeerSelf(), media))


def construct_media(file_id: int, access_hash: int, gif: bool = False):
    if gif:
        return MessageMediaDocument(document=Document(file_id, access_hash, b'', datetime.datetime.now(), mime_type='video/mp4', size=0, dc_id=4, attributes=[]))
    else:
        return MessageMediaPhoto(photo=Photo(file_id, access_hash, b'', datetime.datetime.now(), [], 4))


class Media:
    def __init__(self, path: str):
        self.path = path

        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

    # shorthands
    def db_exec(self, sql: str, parameters=()) -> sqlite3.Cursor:
        if parameters == ():
            return self.cursor.execute(sql)
        return self.cursor.execute(sql, parameters)

    def db_fetch(self):
        return self.cursor.fetchall()

    def db_fetch_one(self):
        return self.cursor.fetchone()

    async def bot(self, necessary_media_files: Dict[str, str], client: TelegramClient, bot_id: int = None) -> BotMedia:
        if bot_id is None:
            bot_id = (await client.get_me()).id

        # literally unreadable
        self.db_exec(f"CREATE TABLE IF NOT EXISTS \"{NECESSARY_TABLE}{bot_id}\" ("
                     "\"name\" int NOT NULL, \"file_id\" int, PRIMARY KEY (name));")

        self.db_exec(f"CREATE TABLE IF NOT EXISTS \"{UPLOADS_TABLE}{bot_id}\" ("
                     "\"file_id\" int NOT NULL, \"access_hash\" int NOT NULL, PRIMARY KEY (file_id));")

        self.db_exec(f"SELECT * FROM {NECESSARY_TABLE}{bot_id}")

        necessary_table = {row[0]: row[1] for row in self.db_fetch()}
        necessary_media = {}

        parent_folder = ''

        if PARENT_FOLDER_KEY in necessary_media_files.keys():
            parent_folder = necessary_media_files[PARENT_FOLDER_KEY]

        for name, path in necessary_media_files.items():
            if name in [PARENT_FOLDER_KEY, GIFS_KEY]:
                continue

            gif = name in necessary_media_files[GIFS_KEY]

            if path[0] == '.':
                path = name + path

            path = parent_folder + ('/' if parent_folder[-1] != '/' else '') + path

            if name in necessary_table.keys():
                file_id = necessary_table[name]
                if file_id is not None:
                    self.db_exec(f"SELECT access_hash FROM {UPLOADS_TABLE}{bot_id} "
                                 f"WHERE file_id = \"{file_id}\"")
                    necessary_media[name] = construct_media(file_id, self.db_fetch_one()[0], gif)
                    continue

            media = await upload_media(client, path, gif)
            file_id = media.photo.id if type(media) == MessageMediaPhoto else media.document.id
            access_hash = media.photo.access_hash if type(media) == MessageMediaPhoto else media.document.access_hash

            self.db_exec(f"INSERT OR REPLACE INTO {UPLOADS_TABLE}{bot_id} (file_id, access_hash) VALUES (?, ?)",
                         (file_id, access_hash))
            self.db_exec(f"INSERT OR REPLACE INTO {NECESSARY_TABLE}{bot_id} (name, file_id) VALUES (?, ?)",
                         (name, file_id))

            necessary_media[name] = construct_media(file_id, access_hash, gif)

        self.connection.commit()

        return BotMedia(necessary_media)
