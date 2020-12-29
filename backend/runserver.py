from waitress import serve

from api.app import APIService
from api.config import load_config_file

cfg = load_config_file()
api_app = APIService(cfg)

serve(api_app, listen="*:8000")
