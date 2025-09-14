from pathlib import Path

from weather_api.app.core import App
from weather_api.configs import Configs
from weather_api.services.cache import Cache
from weather_api.services.local_dynamo_db import LocalEventLog
from weather_api.services.local_s3_storage import LocalStorage

# main server processors
configs = Configs(package_dir=Path(__file__).parent)
app = App(configs=configs)
local_storage = LocalStorage()
local_event_log = LocalEventLog()
cache = Cache(configs.redis.dsn)
