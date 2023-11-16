import json
from typing import List, Union


class BotConfig:
    BOT = {'data', 'lang', 'media', 'logging', 'auth', 'testing'}
    CLONE = {'clone_of', 'auth'}
    AUTH = {'session', 'app_id', 'app_hash', 'token'}

    def __init__(self, json: dict, clone_of: dict = None):
        if (self.BOT ^ json.keys() != set() and clone_of is None) or (self.CLONE ^ json.keys() != set() and clone_of is not None):
            raise Exception('Incorrect bot config')

        if self.AUTH ^ json['auth'].keys() != set():
            raise Exception('Incorrect bot auth config')

        # auth
        self.session: str = json['auth']['session']
        self.app_id: int = json['auth']['app_id']
        self.app_hash: str = json['auth']['app_hash']
        self.token: str = json['auth']['token']

        config = json if clone_of is None else clone_of

        # info
        self.testing: bool = config['testing']

        # other
        self.db_path: str = config['data']
        self.lang_config_path: str = config['lang']
        self.media: str = config['media']
        self.necessary_media: str = config['necessary_media']
        self.logging: dict = config['logging']


class Config:
    def __init__(self, path: str):
        self.path: str = path
        self.json: dict = json.load(open(self.path, 'r'))

        self.bots: List[BotConfig] = [BotConfig(bot_config_json) for bot_config_json in self.json['bots']]
        self.testing: bool = self.json['testing']
