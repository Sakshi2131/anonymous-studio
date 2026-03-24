"""Tests for mongo_persistence module."""

from unittest.mock import patch, MagicMock
import pytest

import mongo_persistence


def test_get_database_raises_without_uri():
    """get_database raises ValueError when MONGODB_URI is not set."""
    mongo_persistence._get_client.cache_clear()
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError, match="MONGODB_URI is not set"):
            mongo_persistence.get_database()


def test_get_database_default_name():
    """get_database uses 'anonymous_studio' when no override is given."""
    mongo_persistence._get_client.cache_clear()
    fake_client = MagicMock()
    with patch("mongo_persistence.MongoClient", return_value=fake_client):
        with patch.dict("os.environ", {"MONGODB_URI": "mongodb://localhost"}, clear=True):
            mongo_persistence.get_database()
            fake_client.__getitem__.assert_called_with("anonymous_studio")


def test_get_database_env_name():
    """get_database reads MONGODB_DB_NAME from the environment."""
    mongo_persistence._get_client.cache_clear()
    fake_client = MagicMock()
    env = {"MONGODB_URI": "mongodb://localhost", "MONGODB_DB_NAME": "custom_db"}
    with patch("mongo_persistence.MongoClient", return_value=fake_client):
        with patch.dict("os.environ", env, clear=True):
            mongo_persistence.get_database()
            fake_client.__getitem__.assert_called_with("custom_db")


def test_get_database_param_overrides_env():
    """Explicit db_name parameter takes precedence over env var."""
    mongo_persistence._get_client.cache_clear()
    fake_client = MagicMock()
    env = {"MONGODB_URI": "mongodb://localhost", "MONGODB_DB_NAME": "env_db"}
    with patch("mongo_persistence.MongoClient", return_value=fake_client):
        with patch.dict("os.environ", env, clear=True):
            mongo_persistence.get_database("override_db")
            fake_client.__getitem__.assert_called_with("override_db")


def test_ping_success():
    """ping returns True when the cluster is reachable."""
    mongo_persistence._get_client.cache_clear()
    fake_client = MagicMock()
    with patch("mongo_persistence.MongoClient", return_value=fake_client):
        with patch.dict("os.environ", {"MONGODB_URI": "mongodb://localhost"}):
            assert mongo_persistence.ping() is True
            fake_client.admin.command.assert_called_with("ping")


def test_ping_failure():
    """ping returns False when the cluster is unreachable."""
    mongo_persistence._get_client.cache_clear()
    fake_client = MagicMock()
    fake_client.admin.command.side_effect = mongo_persistence.ConnectionFailure("down")
    with patch("mongo_persistence.MongoClient", return_value=fake_client):
        with patch.dict("os.environ", {"MONGODB_URI": "mongodb://localhost"}):
            assert mongo_persistence.ping() is False
