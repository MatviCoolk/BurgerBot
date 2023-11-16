import json
from typing import List, Union, Dict


class BotConfig:
    BOT = {'data', 'lang', 'media', 'logging', 'auth', 'testing', 'necessary_media'}
    CLONE = {'auth'}
    AUTH = {'session', 'app_id', 'app_hash', 'token'}

    def __init__(self, config: dict, clone_of: dict = None):
        if (self.BOT ^ config.keys() != set() and clone_of is None) or (self.CLONE ^ config.keys() != set() and clone_of is not None):
            raise Exception('Incorrect bot config')

        if self.AUTH ^ config['auth'].keys() != set():
            raise Exception('Incorrect bot auth config')

        # auth
        self.session: str = config['auth']['session']
        self.app_id: int = config['auth']['app_id']
        self.app_hash: str = config['auth']['app_hash']
        self.token: str = config['auth']['token']

        config = config if clone_of is None else clone_of

        # info
        self.testing: bool = config['testing']

        # other
        self.db_path: str = config['data']
        self.lang_config_path: str = config['lang']
        self.media: str = config['media']
        self.necessary_media: str = config['necessary_media']
        self.logging: dict = config['logging']

        self.json = config


class Config:
    def __init__(self, path: str):
        self.path: str = path
        self.json: dict = json.load(open(self.path, 'r'))

        main_bots = {bot_config[0]: BotConfig(bot_config[1]) for bot_config in self.json['bots'].items()}

        self.bots: Dict[str: BotConfig] = list(main_bots.values())

        for main, clones in self.json['clones'].items():
            for clone in clones:
                self.bots.append(BotConfig(clone, main_bots[main].json))

        self.testing: bool = self.json['testing']
