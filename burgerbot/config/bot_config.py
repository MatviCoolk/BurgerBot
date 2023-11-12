from typing import Union


class BotConfig:
    REQUIRED_VALUES = {'data', 'lang', 'media', 'logging', 'auth', 'testing'}
    REQUIRED_AUTH_VALUES = {'session', 'app_id', 'app_hash', 'token'}

    def __init__(self, json: dict):
        if self.REQUIRED_VALUES & json.keys() != self.REQUIRED_VALUES:
            raise KeyError('Not enough values for bot config')

        if self.REQUIRED_AUTH_VALUES & json['auth'].keys() != self.REQUIRED_AUTH_VALUES:
            raise KeyError('Not enough values for bot auth config')

        # auth
        self.session: str = json['auth']['session']
        self.app_id: int = json['auth']['app_id']
        self.app_hash: str = json['auth']['app_hash']
        self.token: str = json['auth']['token']
        self.username: Union[str, None] = json['auth'].get('username')

        # info
        self.testing: bool = json['testing']

        # other
        self.db_path: str = json['data']
        self.lang_config_path: str = json['lang']
        self.media: str = json['media']
        self.necessary_media: str = json['necessary_media']
        self.logging: dict = json['logging']

