import aumbry
from waitress import serve

from api.app import APIService
from api.config import AppConfig

cfg = aumbry.load(aumbry.FILE, AppConfig, {'CONFIG_FILE_PATH': './config.json'})
api_app = APIService(cfg)

serve(api_app, listen='*:8000')
