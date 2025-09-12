from dataclasses import dataclass
from pathlib import Path

import aiosqlite


@dataclass
class EventRecord:
    city: str
    timestamp: str
    path: str


class LocalEventLog:
    """SQLite-based async log using aiosqlite"""


    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / "Event_log"
        self.db_path.mkdir(parents=True, exist_ok=True)
        self._conn: aiosqlite.Connection | None
        self._ready = False


    async def _ensure_ready(self) -> None:
        if not self._ready:
            self._conn = await aiosqlite.connect(Path(self.db_path) / "events.db")
            await self._conn.execute(
            """
                CREATE TABLE IF NOT EXISTS weather_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                path TEXT NOT NULL,
                UNIQUE(city, timestamp)
                )
            """
            )
            await self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_weather_events_ts ON weather_events(timestamp)"
            )
            await self._conn.commit()
            self._ready = True


    async def put(self, record: EventRecord) -> None:
        await self._ensure_ready()
        assert self._conn is not None
        await self._conn.execute(
            "INSERT OR REPLACE INTO weather_events (city, timestamp, path) VALUES (?, ?, ?)",
            (record.city, record.timestamp, record.path),
        )
        await self._conn.commit()

    async def get_latest(self, city: str) -> EventRecord | None:
        await self._ensure_ready()

        assert self._conn is not None
        cursor = await self._conn.execute(
            "SELECT city, timestamp, path FROM weather_events WHERE city = ? ORDER BY timestamp DESC LIMIT 1",
            (city,),
        )
        row = await cursor.fetchone()
        await cursor.close()
        if not row:
            return None
        return EventRecord(city=row[0], timestamp=row[1], path=row[2])


    async def close(self) -> None:
        if self._conn is not None:
            await self._conn.close()
            self._conn = None
            self._ready = False