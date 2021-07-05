from pathlib import Path
import configparser


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()

        # Check if config exists and read it in or create a default
        if Path("config.ini").is_file():
            self.config.read("config.ini")
        else:
            self.config['FILE PATHS'] = {'inputXml': 'None',
                                         'outputXml': 'None'}
            self.config['PARSE SETTINGS'] = {'pollRate': '1'}
            self.config['GENERAL'] = {'debug': "false"}
            self._write_config()

    def contains(self, header: str, key: str) -> bool:
        if header in self.config:
            if key in self.config[header]:
                return True
        return False

    def get(self, header: str, key: str) -> str:
        return self.config.get(header, key)

    def update(self, header: str, key: str, value: str):
        self.config.set(header, key, value)
        self._write_config()

    def _write_config(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
