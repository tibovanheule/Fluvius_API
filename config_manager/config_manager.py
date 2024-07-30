import configparser
from pathlib import Path


class ConfigManager():
    """
    Helper class to manage the configuration of the package. It will help read the configuration or help write the configuration file.
    """

    def __init__(self):
        """
        Constructor for the ConfigManager class. This will initialise the configuration of the package, if a config.ini file is present.
        """
        self.config = configparser.ConfigParser()
        config_path = Path("config.ini")
        if config_path.is_file():
            self.config.read('config.ini')

    def create(self, login, password, ean, browser):
        self.config.write("fluvius")

    def get(self, *args, **kwargs):
        return self.config.get(*args, **kwargs)
