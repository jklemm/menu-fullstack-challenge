import aumbry
from aumbry import Attr, JsonConfig


class DatabaseConfig(JsonConfig):
    __mapping__ = {
        "connection": Attr("connection", str),
    }

    connection = ""


class AppConfig(JsonConfig):
    __mapping__ = {
        "db": Attr("db", DatabaseConfig),
        "db_test": Attr("db_test", DatabaseConfig),
        "db_ci_test": Attr("db_ci_test", DatabaseConfig),
        "gunicorn": Attr("gunicorn", dict),
    }

    def __init__(self):
        self.db = DatabaseConfig()
        self.db_test = DatabaseConfig()
        self.db_ci_test = DatabaseConfig()
        self.gunicorn = {}


def load_config_file():
    return aumbry.load(aumbry.FILE, AppConfig, {"CONFIG_FILE_PATH": "./config.json"})
