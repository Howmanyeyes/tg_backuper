"""Module with class "Config" that is used to easely interact with user's config"""

import json

DEFAULT_SETTINGS = {
    "API": "",
    "chats": [],
    "paths": [],
    "time": 0,
    "frequency": {
        "every_day": True,
        "week_days": []
    }
}

class Config:
    """Class with easy way to interact with user's config"""

    path = "back_end/changable_data/settings.json"

    def __init__(self):
        """Init function"""
        self.config = {}
        self.load()

    def load(self):
        """Internal function for loading/creating config from file"""
        try:
            with open(self.path, 'r', encoding = 'utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            settings_json = json.dumps(DEFAULT_SETTINGS, indent=4)
            with open(self.path, "w", encoding = 'utf-8') as f:
                f.write(settings_json)
            self.config = DEFAULT_SETTINGS

    def save(self):
        """Saves internal self.config to config file"""
        settings_json = json.dumps(self.config, indent=4)
        with open(self.path, 'w', encoding = 'utf-8') as f:
            f.write(settings_json)

    def export(self, data_type : str):
        """Exports config as python dict"""
        if data_type == 'dict':
            return self.config
        return json.dumps(self.config, indent=4)

    def edit_dict(self, new_config, data_type : str):
        """Changes config to one, that has been passed"""
        if data_type == 'dict':
            self.config = new_config
        else:
            self.config = json.loads(new_config)
        self.save()

    @property
    def api(self):
        """Returns API key"""
        return self.config["API"]

config = Config()
