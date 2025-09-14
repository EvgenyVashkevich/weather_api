import json
import logging

from redis.asyncio import Redis

from weather_api.services.scheme import WeatherResponse

logger = logging.getLogger(__name__)

CACHE_PREFIX = "initial_impl_weather_api"


class Cache:
    def __init__(self, redis_url: str):
        self.cache = Redis.from_url(redis_url, encoding="utf-8", decode_responses=True)

    async def get(self, city: str) -> WeatherResponse | None:
        key = f"{CACHE_PREFIX}:{city}"
        try:
            raw = await self.cache.get(key)
            if not raw:
                return None
            data = json.loads(raw)
            return WeatherResponse.model_validate(data)
        except Exception as e:  # pragma: no cover
            logger.warning("cache get failed: %s", e)
            return None

    async def set(self, city: str, cache_ttl_seconds: int, payload: WeatherResponse) -> None:
        key = f"{CACHE_PREFIX}:{city}"
        try:
            await self.cache.setex(
                key, cache_ttl_seconds, json.dumps(payload.model_dump(), ensure_ascii=False)
            )
        except Exception as e:
            logger.warning("cache set failed: %s", e)
