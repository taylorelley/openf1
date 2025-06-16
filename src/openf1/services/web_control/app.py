from __future__ import annotations

import subprocess
import os
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from loguru import logger


templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Year used when ingesting historical data via the control panel.
HISTORICAL_YEAR = os.getenv("OPENF1_HISTORICAL_SEASON", "2024")

# Base commands used to launch the services. For services that accept runtime
# options, parameters can be injected before starting the process.
BASE_SERVICES: dict[str, list[str]] = {
    "query_api": [
        "uvicorn",
        "openf1.services.query_api.app:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8001",
    ],
    "ingestor_real_time": [
        "python",
        "-m",
        "openf1.services.ingestor_livetiming.real_time.app",
    ],
    "ingestor_historical": [
        "python",
        "-m",
        "openf1.services.ingestor_livetiming.historical.main",
        "ingest-season",
    ],
}

# Running processes keyed by service name.
running_processes: dict[str, subprocess.Popen] = {}


def get_service_cmd(name: str, *, year: str | None = None) -> list[str] | None:
    """Return the command list for a service with optional parameters."""
    base_cmd = BASE_SERVICES.get(name)
    if not base_cmd:
        return None

    cmd = list(base_cmd)
    if name == "ingestor_historical":
        cmd.append(str(year or HISTORICAL_YEAR))

    return cmd

app = FastAPI(title="OpenF1 Control Panel")


def start_service(name: str, *, year: str | None = None) -> None:
    if name in running_processes:
        logger.info(f"Service {name} already running")
        return
    cmd = get_service_cmd(name, year=year)
    if not cmd:
        logger.warning(f"Unknown service: {name}")
        return
    logger.info(f"Starting service {name}: {' '.join(cmd)}")
    running_processes[name] = subprocess.Popen(cmd)


def stop_service(name: str) -> None:
    process = running_processes.get(name)
    if not process:
        logger.info(f"Service {name} not running")
        return
    logger.info(f"Stopping service {name}")
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
    del running_processes[name]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    statuses = {name: name in running_processes for name in BASE_SERVICES}
    context = {
        "request": request,
        "services": statuses,
        "historical_year": HISTORICAL_YEAR,
    }
    return templates.TemplateResponse("index.html", context)


@app.post("/control")
async def control(
    name: str = Form(...),
    action: str = Form(...),
    year: str | None = Form(None),
):
    if action == "start":
        start_service(name, year=year)
    elif action == "stop":
        stop_service(name)
    return RedirectResponse(url="/", status_code=303)
