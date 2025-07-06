# OpenF1 API

**OpenF1** is a free and open-source API that offers real-time and historical Formula 1 data.<br />
Whether you're a developer, data analyst, or F1 enthusiast, OpenF1 provides comprehensive
access to lap timings, car telemetry, driver information, race control messages, and more.

Explore the data through JSON or CSV formats to build dashboards, analyze races, or
integrate F1 data into your projects.

For full API documentation, visit [openf1.org](https://openf1.org).

## Key Features

- **Real-Time Data**: Stay updated with live lap times, speeds, and driver positioning.
- **Historical Data**: Analyze past races, compare performance over seasons, and dive deep into race strategy.
- **Car Telemetry**: Access in-depth car data, including throttle, brake, DRS, and gear information.
- **Driver Information**: Get details on F1 drivers, including team affiliations and performance metrics.

## Example Usage

Here’s a quick example of how to fetch lap data for a specific driver using the API:

```bash
curl "https://api.openf1.org/v1/laps?session_key=9161&driver_number=63&lap_number=8"
```

For more detailed examples and documentation, visit the [API Documentation](https://openf1.org).

## Running the project locally

1. Install and start [MongoDB Community Server](https://www.mongodb.com/try/download/community) v7

2. Install pip>=23 and python>=3.10

3. Install the OpenF1 python package

```bash
git clone git@github.com:br-g/openf1.git
pip install -e openf1
```

4. Configure the MongoDB connection

Set the **MONGO_CONNECTION_STRING** environment variable to connect to your local MongoDB instance:

```bash
export MONGO_CONNECTION_STRING="mongodb://localhost:27017"
```

5. Run the project

- Fetch and ingest data: [services/ingestor_livetiming/](src/openf1/services/ingestor_livetiming/README.md)
- Start and query the API: [services/query_api/](src/openf1/services/query_api/README.md)

## MongoDB indexes

OpenF1 queries rely on indexes for efficient lookups. Each collection should at
least have single-field indexes on:

- `_key`
- `date_start`
- `meeting_key`
- `session_key`

When running the project via Docker Compose, the control panel automatically
creates these indexes on startup. For manual setups, run the following command
to add them if they are missing:

```bash
python -m openf1.util.create_mongo_indexes
```

## Running with Docker Compose

The repository includes a `docker-compose.yml` file that sets up MongoDB and starts the OpenF1 control panel.
After installing [Docker](https://docs.docker.com/get-docker/) run:

```bash
docker compose up --build
```

The control panel will be available at [http://localhost:9876](http://localhost:9876).
Start the "Query API" service from the panel to access the API at [http://localhost:9877](http://localhost:9877).
You can also set the desired season year for historical ingestion directly from the panel.
The panel additionally exposes a **live_recorder** service which records the raw timing feed, ingests it into MongoDB and stores it locally using the same format as the historical files.

## Supporting OpenF1

If you find this project useful, consider supporting its long-term sustainability:

<div>
  <a href="https://www.buymeacoffee.com/openf1" target="_blank" style="text-decoration:none; border:none;">
    <img src="https://storage.googleapis.com/openf1-public/images/bmec_button.png" alt="Buy Me A Coffee" height="32" style="border:none; vertical-align:middle;">
  </a>
  &nbsp;
  <a href="https://github.com/sponsors/br-g" style="text-decoration:none; border:none;">
    <img src="https://img.shields.io/badge/Sponsor-%E2%9D%A4-brightgreen" alt="Sponsor me" height="32" style="border:none; vertical-align:middle;">
  </a>
</div>

## Disclaimer

OpenF1 is an unofficial project and is not affiliated with Formula 1 companies.
All F1-related trademarks are owned by Formula One Licensing B.V.
