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
        "gunicorn": Attr("gunicorn", dict),
    }

    def __init__(self):
        self.db = DatabaseConfig()
        self.db_test = DatabaseConfig()
        self.gunicorn = {}
