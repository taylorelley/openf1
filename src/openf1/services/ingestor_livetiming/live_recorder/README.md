# Live Recorder

This utility records live timing data to a file **while ingesting it into MongoDB**.
The raw file is converted to the same `.jsonStream` format as the official
historical data and saved under the standard `historical/<year>/<meeting_key>/<session_key>`
directory so it can be used as a drop-in replacement until the official files
become available.

## Running

```bash
python -m openf1.services.ingestor_livetiming.live_recorder.app
```

The temporary recording is saved under `OPENF1_CACHE_DIR/live_recordings/`. Once
the run finishes, the data are moved to `OPENF1_CACHE_DIR/historical/<year>/<meeting_key>/<session_key>`
with one `.jsonStream` file per topic.
