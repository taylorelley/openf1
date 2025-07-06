import asyncio
import ast
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from loguru import logger

from openf1.services.ingestor_livetiming.core.objects import get_topics
from openf1.services.ingestor_livetiming.real_time.processing import ingest_file
from openf1.services.ingestor_livetiming.real_time.recording import record_to_file
from openf1.util.misc import to_datetime

CACHE_DIR = Path(os.getenv("OPENF1_CACHE_DIR", Path.home() / ".cache" / "openf1"))
RECORDINGS_DIR = CACHE_DIR / "live_recordings"
TIMEOUT = 10800  # 3 hours


def _format_timedelta(delta: timedelta) -> str:
    total_ms = int(delta.total_seconds() * 1000)
    hours = total_ms // 3_600_000
    minutes = (total_ms % 3_600_000) // 60_000
    seconds = (total_ms % 60_000) // 1000
    ms = total_ms % 1000
    return f"{hours}:{minutes:02}:{seconds:02}.{ms:03}"


def convert_recording_to_jsonstreams(source: Path) -> Path:
    """Convert raw fastf1-livetiming output to F1-like jsonStream files.

    Returns the directory containing the converted files."""
    output_dir = source.with_suffix("")
    output_dir.mkdir(parents=True, exist_ok=True)

    handles: dict[str, Path] = {}
    t0 = None
    meeting_key = None
    session_key = None
    year = None

    with source.open("r") as f:
        for line in f:
            if not line.strip():
                continue
            topic, content, ts = ast.literal_eval(line)
            ts_dt = to_datetime(ts)
            if ts_dt is None:
                continue

            if topic == "SessionInfo" and isinstance(content, dict):
                meeting_key = content.get("Meeting", {}).get("Key")
                session_key = content.get("Key")
                start = content.get("StartDate")
                start_dt = to_datetime(start)
                if start_dt is not None:
                    year = start_dt.year

            if t0 is None:
                t0 = ts_dt

            delta = ts_dt - t0
            line_prefix = _format_timedelta(delta)
            if isinstance(content, dict):
                content_str = json.dumps(content, separators=(",", ":"))
            else:
                content_str = str(content)
            fh = handles.get(topic)
            if fh is None:
                fh = (output_dir / f"{topic}.jsonStream").open("w")
                handles[topic] = fh
            fh.write(f"{line_prefix}{content_str}\r\n")

    for fh in handles.values():
        fh.close()

    if meeting_key and session_key and year:
        hist_dir = (
            CACHE_DIR / "historical" / str(year) / str(meeting_key) / str(session_key)
        )
        hist_dir.mkdir(parents=True, exist_ok=True)
        for fpath in output_dir.iterdir():
            fpath.rename(hist_dir / fpath.name)
        output_dir.rmdir()
        output_dir = hist_dir

    return output_dir


async def main():
    RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    file_path = RECORDINGS_DIR / f"{timestamp}.txt"

    logger.info(f"Recording raw data to '{file_path}'")
    tasks = []

    env_topics = os.getenv("OPENF1_LIVE_TOPICS")
    topics = sorted(list(get_topics()))
    if env_topics:
        allowed = {t.strip() for t in env_topics.split(",") if t.strip()}
        topics = [t for t in topics if t in allowed]

    task_recording = asyncio.create_task(
        record_to_file(filepath=str(file_path), topics=topics, timeout=TIMEOUT)
    )
    tasks.append(task_recording)

    task_ingest = asyncio.create_task(ingest_file(str(file_path)))
    tasks.append(task_ingest)

    await asyncio.wait([task_recording], return_when=asyncio.FIRST_COMPLETED)
    logger.info("Recording stopped")

    logger.info("Stopping tasks")
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    logger.info("Job completed")

    logger.info("Converting recording to jsonStream format")
    convert_recording_to_jsonstreams(file_path)


if __name__ == "__main__":
    asyncio.run(main())
