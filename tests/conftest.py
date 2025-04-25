import os
import uuid

import pytest
from flask import Flask
from sqlalchemy import create_engine

from app import create_app


engine = create_engine("sqlite:///test.db", echo=False)

@pytest.fixture()
def app():
    flask_app = create_app(engine, True)
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

def pytest_sessionfinish(session, exitstatus):
    engine.dispose()
    # makes sure db doesn't get deleted if we are testing individual unit tests
    if len(session.items) > 1:
        db_path = "test.db"
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
            except Exception as e:
                print(f"Failed to cleanup database at {db_path} after running the tests: {e}")
