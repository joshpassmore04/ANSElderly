import os
import uuid

import pytest
from flask import Flask
from sqlalchemy import create_engine

from app import create_app


engine = create_engine("sqlite:///test.db", echo=False)

@pytest.fixture()
def app():
    flask_app = create_app(engine)
    flask_app.testing = True
    flask_app.debug = True
    yield flask_app

@pytest.fixture()
def client(app: Flask):
    return app.test_client()

@pytest.fixture()
def endpoint(app: Flask):
    return app.config["ENDPOINT"]

@pytest.fixture()
def port(app: Flask):
    return app.config["PORT"]

def pytest_sessionfinish(exitstatus):
    engine.dispose()

    db_path = "test.db"
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"[pytest cleanup] Deleted {db_path}")
        except Exception as e:
            print(f"[pytest cleanup] Failed to delete {db_path}: {e}")