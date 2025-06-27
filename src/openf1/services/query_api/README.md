# Query API

This module exposes the OpenF1 API.<br />
Upon receiving a request, the service parses the input and formulates a corresponding
query to the MongoDB database, ensuring the proper data is fetched.

### Running the API locally

Start the server in development mode:

```bash
uvicorn openf1.services.query_api.app:app --reload
```

Make a query in the browser: http://127.0.0.1:8000/v1/meetings?year>=2024

When running through Docker Compose and the control panel, the API will be
available on `http://localhost:9877` after starting the service from the panel.

To restrict which collections can be queried, set the
`OPENF1_API_COLLECTIONS` environment variable to a comma separated list of
collection names.
