import logging
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Query, status

from weather_api.app.core import exceptions
from weather_api.processors import cache, local_event_log, local_storage
from weather_api.services import callbacks, errors, scheme
from weather_api.services.local_dynamo_db import EventRecord
from weather_api.services.scheme import WeatherResponse

logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = 300

router = APIRouter(
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": exceptions.ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": exceptions.ErrorResponse},
    }
)


def utc_now() -> datetime:
    return datetime.now(UTC)


def parse_compact_ts(ts: str) -> datetime:
    return datetime.strptime(ts, "%Y%m%dT%H%M%SZ").replace(tzinfo=UTC)


def utc_ts_compact(dt: datetime | None = None) -> tuple[str, str]:
    dt = dt or utc_now()
    return dt.strftime("%Y%m%dT%H%M%SZ"), dt.strftime("%Y-%m-%d %H:%M:%S")


async def try_storage_second_chance(city: str) -> WeatherResponse | None:
    """If enabled, attempt to read the latest stored object if it is fresh (<= TTL)."""
    try:
        rec = await local_event_log.get_latest(city)
        if not rec:
            return None
        age = utc_now() - parse_compact_ts(rec.timestamp)
        if age > timedelta(seconds=CACHE_TTL_SECONDS):
            return None
        payload = await local_storage.read_json(rec.path)
        return WeatherResponse.model_validate(payload)
    except Exception as e:
        logger.warning("second-chance storage read failed: city=%s error=%s", city, e)
        return None


@router.get(
    "",
    summary="Get weather for specified city",
    response_model=scheme.WeatherResponse,
    responses={status.HTTP_404_NOT_FOUND: {"model": errors.NotFound}},
)
async def weather(
    city: str = Query(..., example="Warsaw"),
) -> scheme.WeatherResponse:
    ts, ts_readable = utc_ts_compact()
    city = city.lower()

    # 1. Redis cache check
    cached = await cache.get(city)
    if cached is not None:
        logger.info("cache hit: %s", city)
        return cached

    # 2. Second-chance: read recent object from storage via event log
    second = await try_storage_second_chance(city)
    if second is not None:
        logger.info("second-chance hit from storage: %s", city)
        await cache.set(city, CACHE_TTL_SECONDS, second)
        return second

    # 3. Fetch from provider
    result = await callbacks.weather(city, ts_readable)
    path = await local_storage.store_weather(city, ts, result)
    await local_event_log.put(EventRecord(city=city, timestamp=ts, path=path))
    await cache.set(city, CACHE_TTL_SECONDS, result)
    return result
