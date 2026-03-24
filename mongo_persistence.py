"""MongoDB persistence helpers for Anonymous Studio.

Provides a thin wrapper around pymongo to connect to a MongoDB Atlas
cluster. Configuration is read from environment variables so that
credentials are never hard-coded.

Environment variables
---------------------
MONGODB_URI : str
    Full ``mongodb+srv://`` connection string from Atlas.
MONGODB_DB_NAME : str, optional
    Database name. Defaults to ``anonymous_studio``.
"""

import os
from datetime import datetime, timezone
from functools import lru_cache
from uuid import uuid4

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

load_dotenv()

_DEFAULT_DB_NAME = "anonymous_studio"


@lru_cache(maxsize=1)
def _get_client() -> MongoClient:
    """Return a cached MongoClient instance.

    Raises
    ------
    ValueError
        If ``MONGODB_URI`` is not set.
    """
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise ValueError(
            "MONGODB_URI is not set. "
            "Add it to your .env file — see docs/mongodb-setup.md."
        )
    return MongoClient(
        uri,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        socketTimeoutMS=5000,
    )


def get_database(db_name: str | None = None) -> Database:
    """Return a pymongo Database handle.

    Parameters
    ----------
    db_name : str, optional
        Override the default database name.

    Returns
    -------
    pymongo.database.Database
    """
    name = db_name or os.getenv("MONGODB_DB_NAME", _DEFAULT_DB_NAME)
    return _get_client()[name]


def ping() -> bool:
    """Return ``True`` if the MongoDB cluster is reachable."""
    try:
        _get_client().admin.command("ping")
        return True
    except ConnectionFailure:
        return False


def create_card(title: str, actor: str = "system") -> dict:
    """Create a new pipeline card and write an audit log event."""
    cleaned_title = title.strip()
    if not cleaned_title:
        raise ValueError("Card title cannot be empty.")

    db = get_database()
    now = datetime.now(timezone.utc)

    card = {
        "card_id": str(uuid4()),
        "title": cleaned_title,
        "status": "Intake",
        "created_at": now,
        "updated_at": now,
        "actor": actor,
    }

    db.cards.insert_one(card)

    audit_event = {
        "timestamp": now,
        "event_type": "CARD_CREATED",
        "card_id": card["card_id"],
        "actor": actor,
        "before_state": None,
        "after_state": "Intake",
        "metadata": {"title": card["title"]},
    }
    db.audit_logs.insert_one(audit_event)

    return card


def get_cards_by_status(status: str) -> list[dict]:
    """Return all cards for a single workflow stage."""
    db = get_database()
    return list(db.cards.find({"status": status}).sort("created_at", 1))


def get_all_cards() -> list[dict]:
    """Return all pipeline cards."""
    db = get_database()
    return list(db.cards.find().sort("created_at", 1))