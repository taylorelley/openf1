"""Create MongoDB indexes for the OpenF1 database."""

import os

from pymongo import ASCENDING, MongoClient

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
MONGO_DATABASE = os.getenv("OPENF1_DB_NAME", "openf1-livetiming")

INDEX_FIELDS = ["_key", "date_start", "meeting_key", "session_key"]


def create_indexes() -> None:
    """Create indexes if they do not already exist."""
    client = MongoClient(MONGO_CONNECTION_STRING)
    db = client[MONGO_DATABASE]

    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        info = collection.index_information()
        existing_fields = {index["key"][0][0] for index in info.values()}

        for field in INDEX_FIELDS:
            if field not in existing_fields:
                collection.create_index([(field, ASCENDING)])
                print(f"Created index on {collection_name}.{field}")


if __name__ == "__main__":
    create_indexes()
