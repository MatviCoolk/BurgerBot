import json
from typing import List

from burgerbot.config.bot_config import BotConfig


class Config:
    def __init__(self, path: str):
        self.path: str = path
        self.json: dict = json.load(open(self.path, 'r'))

        self.bots: List[BotConfig] = [BotConfig(bot_config_json) for bot_config_json in self.json['bots']]
        self.testing: bool = self.json['testing']
