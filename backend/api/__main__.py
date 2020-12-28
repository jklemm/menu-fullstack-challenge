import aumbry
from gunicorn.app.base import BaseApplication
from gunicorn.workers.sync import SyncWorker

from api.app import APIService
from api.config import AppConfig


class CustomWorker(SyncWorker):
    def handle_quit(self, sig, frame):
        self.app.application.stop(sig)
        super(CustomWorker, self).handle_quit(sig, frame)

    def run(self):
        self.app.application.start()
        super(CustomWorker, self).run()


class GunicornApp(BaseApplication):
    """Custom Gunicorn application
    This allows for us to load gunicorn settings from an external source
    """

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(GunicornApp, self).__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)

        self.cfg.set("worker_class", "example.__main__.CustomWorker")

    def load(self):
        return self.application


def main():
    cfg = aumbry.load(aumbry.FILE, AppConfig, {"CONFIG_FILE_PATH": "./config.json"})

    api_app = APIService(cfg)
    gunicorn_app = GunicornApp(api_app, cfg.gunicorn)

    gunicorn_app.run()
