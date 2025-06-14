# Web Control Panel

This module exposes a very small web interface that can start or stop the
main OpenF1 services.

## Running

Start the panel with `uvicorn`:

```bash
uvicorn openf1.services.web_control.app:app --reload
```

Open `http://127.0.0.1:8000` in a browser to access the control panel.
