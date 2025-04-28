import random
from datetime import datetime, timedelta

import pytest

from data.permission import PermissionType
from tests.conftest import port

def login_user(client, url, email, password):
    return client.post(url, json={"email": email, "password": password})

def register_user(client, url, email, first_name, last_name, password):
    return client.post(url, json={"email": email, "password": password, "first_name": first_name, "last_name": last_name})

@pytest.fixture
def registered_admin(client, app, endpoint, port):
    register_url = f"http://localhost:{port}{endpoint}user/register"
    register_response = register_user(client, register_url, "admin@test.com", "john", "admin", "adminpassword")
    assert register_response.status_code == 200
    assert register_response.json.get("status") == "success"
    user_id = register_response.json.get("session").get("id")
    assert user_id is not None
    return user_id

def login_user_admin(client, app, endpoint, port):
    login_url = f"http://localhost:{port}{endpoint}user/login"
    login_response = login_user(client, login_url,"admin@test.com", "adminpassword")
    assert login_response.status_code == 200
    assert login_response.json.get("status") == "success"

def test_give_admin_permission(client, app, endpoint, port, registered_admin):
    permission_url = f"http://localhost:{port}{endpoint}user/permission"
    def post_permission_give(to_id):
        user_update_payload = {
            "to_id": to_id,
            "permission_name": PermissionType.ACCESS_ALL_AIRPORT_INFO,
            "action": "give",
            "debug_bypass": True
        }
        return client.post(permission_url, json=user_update_payload)
    login_user_admin(client, app, endpoint, port)
    permission_result = post_permission_give(registered_admin)
    assert permission_result.json.get("status") == "success"


@pytest.fixture
def location_id(client, app, endpoint, port):
    location_url = f"http://localhost:{port}{endpoint}airport/create-location"
    login_user_admin(client, app, endpoint, port)
    location_payload = {
        "latitude": random.uniform(-90, 90),
        "longitude": random.uniform(-180, 180),
        "name": "test"
    }
    location_response = client.post(location_url, json=location_payload)
    print(location_response.json)
    assert location_response.status_code == 200
    assert location_response.json.get("status") == "success"
    return location_response.json.get("location").get("id")

@pytest.fixture
def airport_id(client, app, endpoint, port, location_id):
    airport_url = f"http://localhost:{port}{endpoint}airport/create-airport"
    airport_payload = {
        "name": "test",
        "location_id": location_id,
    }
    airport_response = client.post(airport_url, json=airport_payload)
    assert airport_response.status_code == 200
    assert airport_response.json.get("status") == "success"
    return airport_response.json.get("id")

@pytest.fixture
def second_location_id(client, app, endpoint, port):
    location_url = f"http://localhost:{port}{endpoint}airport/create-location"
    login_user_admin(client, app, endpoint, port)
    location_payload = {
        "latitude": random.uniform(-90, 90),
        "longitude": random.uniform(-180, 180),
        "name": "test-second-location"
    }
    location_response = client.post(location_url, json=location_payload)
    assert location_response.status_code == 200
    assert location_response.json.get("status") == "success"
    return location_response.json.get("id")

@pytest.fixture
def second_airport_id(client, app, endpoint, port, second_location_id):
    airport_url = f"http://localhost:{port}{endpoint}airport/create-airport"
    airport_payload = {
        "name": "test-second-airport",
        "location_id": second_location_id,
    }
    airport_response = client.post(airport_url, json=airport_payload)
    assert airport_response.status_code == 200
    assert airport_response.json.get("status") == "success"
    return airport_response.json.get("id")

@pytest.fixture
def gate_id(client, app, endpoint, port, location_id):
    gate_url = f"http://localhost:{port}{endpoint}airport/create-gate"
    gate_payload = {
        "number": random.randint(1, 100),
        "opening_time": (datetime.now() + timedelta(hours=1)).isoformat(),  # Gate opens 1h from now
        "location_id": location_id,
    }
    gate_response = client.post(gate_url, json=gate_payload)
    assert gate_response.status_code == 200
    assert gate_response.json.get("status") == "success"
    return gate_response.json.get("id")

@pytest.fixture
def aircraft_id(client, app, endpoint, port, location_id):
    aircraft_url = f"http://localhost:{port}{endpoint}airport/create-aircraft"
    aircraft_payload = {
        "name": f"Test Aircraft {random.randint(1000,9999)}",
        "capacity": random.randint(50, 300),
        "location_id": location_id,
    }
    aircraft_response = client.post(aircraft_url, json=aircraft_payload)
    assert aircraft_response.status_code == 200
    assert aircraft_response.json.get("status") == "success"
    return aircraft_response.json.get("id")


def test_create_airport(client, app, endpoint, port, location_id, airport_id, second_airport_id, aircraft_id, gate_id):
    login_user_admin(client, app, endpoint, port)

    create_airport_url = f"http://localhost:{port}{endpoint}airport/create-airport"

    departure_time = datetime.now() + timedelta(days=1)
    arrival_time = departure_time + timedelta(hours=2)
    print(location_id)

    airport_payload = {
        "from_airport_id": airport_id,
        "to_airport_id": second_airport_id,
        "aircraft_id": aircraft_id,
        "gate_id": gate_id,
        "departure_time": departure_time.isoformat(),
        "arrival_time": arrival_time.isoformat(),
        "location_id": location_id,
        "number": f"FL{random.randint(1000, 9999)}",
    }

    airport_response = client.post(create_airport_url, json=airport_payload)

    assert airport_response.status_code == 200
    json_data = airport_response.json
    assert json_data.get("status") == "success"
    assert json_data.get("id") is not None

