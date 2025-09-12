import json
import os
from pathlib import Path

import aiofiles

from weather_api.services.scheme import WeatherResponse


class LocalStorage:
    def __init__(self):
        self.storage_dir = Path(__file__).parent.parent.parent / "S3_local"
        self.storage_dir.mkdir(parents=True, exist_ok=True)


    async def store_weather(self, city: str, ts: str,  payload: WeatherResponse) -> str:
        filename = f"{city}_{ts}.json"
        path = os.path.join(self.storage_dir, filename)
        body = json.dumps(payload.model_dump(), ensure_ascii=False, indent=2)
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(body)
        return path


    @staticmethod
    async def read_json(path_or_key: str) -> dict:
        path = path_or_key
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            txt = await f.read()
        return json.loads(txt)