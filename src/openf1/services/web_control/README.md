# Web Control Panel

This module exposes a very small web interface that can start or stop the
main OpenF1 services.
It also lets you choose which topics are recorded by the collectors and which
API endpoints are exposed.

## Running

Start the panel with `uvicorn`:

```bash
uvicorn openf1.services.web_control.app:app --reload
```

Open `http://127.0.0.1:8000` in a browser to access the control panel. When run
inside Docker Compose, the panel is available at `http://localhost:9876` and the
Query API starts on port `9877`.

By default, the "ingestor_historical" service ingests data for season `2024`.
Set the `OPENF1_HISTORICAL_SEASON` environment variable to override this year.
You can also specify the desired season directly from the control panel before
starting the service.

The panel exposes settings to select the topics recorded by both collectors as
well as the list of available API endpoints. These settings are stored in the
`OPENF1_LIVE_TOPICS`, `OPENF1_HIST_TOPICS` and `OPENF1_API_COLLECTIONS`
environment variables respectively.
