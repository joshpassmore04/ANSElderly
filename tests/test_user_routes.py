from data.permission import PermissionType


def register_user(client, url, email, first_name, last_name, password):
    return client.post(url, json={"email": email, "password": password, "first_name": first_name, "last_name": last_name})

# Helper function to send login requests
def login_user(client, url, email, password):
    return client.post(url, json={"email": email, "password": password})

# Helper function to perform a @me request
def get_me(client, url):
    return client.get(url)

def test_new_registration(client, app, endpoint, port):
    url = f"http://localhost:{port}{endpoint}user/register"
    print(url)
    with app.app_context():
        response = register_user(client, url, "test@test.com", "john", "smith", "testpassword")
        print(response.data)  # Print the raw response data
        assert response.status_code == 200
        assert response.json.get("status") == "success"

def test_existing_registration(client, app, endpoint, port):
    url = f"http://localhost:{port}{endpoint}user/register"
    with app.app_context():
        # First, register the user
        register_user(client, url, "test@test.com", "john", "smith", "testpassword")

        # Now try registering the same user
        response = register_user(client, url, "test@test.com", "john", "smith", "testpassword")

        # Check if the response code is an error (400 for bad request)
        assert response.status_code == 400
        assert response.json.get("status") == "error"
        assert response.json.get("message") == "Invalid data provided"

def test_invalid_registration(client, app, endpoint, port):
    url = f"http://localhost:{port}{endpoint}user/register"
    with app.app_context():
        # Invalid email
        response = register_user(client, url, "test @abcdefb", "dsjkfs", "sdfdsjfs", "testpassword")
        # Check if the response code is an error (400 for bad request)
        assert response.status_code == 400
        assert response.json.get("status") == "error"
        assert response.json.get("message") == "Invalid data provided"

        # No password
        response = register_user(client, url, "test@test.com", "jfsjdfs", "sdfdsjfs", "")
        # Check if the response code is an error (400 for bad request)
        assert response.status_code == 400
        assert response.json.get("status") == "error"
        assert response.json.get("message") == "Invalid data provided"

        # No username
        response = register_user(client, url, "test@test.com", "", "", "testpassword")
        # Check if the response code is an error (400 for bad request)
        assert response.status_code == 400
        assert response.json.get("status") == "error"
        assert response.json.get("message") == "Invalid data provided"

def test_existing_login(client, app, endpoint, port):
    login_url = f"http://localhost:{port}{endpoint}user/login"
    register_url = f"http://localhost:{port}{endpoint}user/register"
    with app.app_context():
        # # First, register the user
        # response = register_user(client, register_url, "test@test.com", "john", "smith", "testpassword")
        # assert response.status_code == 200
        response = login_user(client, login_url, "test@test.com",  "testpassword")
        assert response.status_code == 200
        assert response.json.get("status") == "success"


def test_invalid_login(client, app, endpoint, port):
    url = f"http://localhost:{port}{endpoint}user/login"
    with app.app_context():
        # Incorrect password
        response = login_user(client, url, "test@test.com",  "testpassword1234")
        # Check if the response code is an error (400 for bad request)
        assert response.status_code == 400
        assert response.json.get("status") == "error"
        assert response.json.get("message") == "Invalid data provided"

        # Incorrect email
        response = login_user(client, url, "test2@test.com",  "testpassword")
        # Check if the response code is an error (400 for bad request)
        assert response.status_code == 400
        assert response.json.get("status") == "error"
        assert response.json.get("message") == "Invalid data provided"


def test_session(client, app, endpoint, port):
    login_url = f"http://localhost:{port}{endpoint}user/login"


    with app.test_client() as test_client:
        with app.app_context():
            # Perform login request
            login_response = login_user(test_client, login_url, "test@test.com", "testpassword")

            # Assert login is successful
            assert login_response.status_code == 200
            assert login_response.json.get("status") == "success"

            # Manually set session cookie in the test client (if needed)
            with test_client.session_transaction() as session:
                session["USER_ID"] = login_response.json["session"]["id"]

            # Make the @me request
            me_url = f"http://localhost:{port}{endpoint}user/@me"
            me_response = get_me(test_client, me_url)

            # Assert the response is successful
            assert me_response.status_code == 200
            assert me_response.json.get("status") == "success"

            # Verify user ID
            assert me_response.json.get("user")["id"] == login_response.json["session"]["id"]


# Test the 'give' permission functionality
def test_permission_give(client, app, endpoint, port):
    login_url = f"http://localhost:{port}{endpoint}user/login"
    permission_url = f"http://localhost:{port}{endpoint}user/permission"

    with app.app_context():
        def post_permission_give():
            user_update_payload = {
                "to_id": 1,
                "permission_name": PermissionType.ACCESS_ALL_FLIGHTS,
                "action": "give",
                "debug_bypass": True
            }
            return client.post(permission_url, json=user_update_payload)

        # Try unauthenticated request
        update_response = post_permission_give()
        assert update_response.status_code == 401

        # Now log in
        response = login_user(client, login_url, "test@test.com", "testpassword")
        assert response.status_code == 200
        assert response.json.get("status") == "success"

        # First attempt to give permission
        update_response = post_permission_give()
        assert update_response.status_code == 200
        assert update_response.json.get("status") == "success"

        # Second attempt to give permission (should fail)
        update_response = post_permission_give()
        assert update_response.status_code == 400
        assert update_response.json.get("message") == "Permission already exists"


# Test the 'check' permission functionality
def test_permission_check(client, app, endpoint, port):
    login_url = f"http://localhost:{port}{endpoint}user/login"
    permission_url = f"http://localhost:{port}{endpoint}user/permission"

    with app.app_context():
        def post_permission_check():
            user_update_payload = {
                "to_id": 1,
                "permission_name": PermissionType.ACCESS_ALL_FLIGHTS,
                "action": "check_current_user",
                "debug_bypass": True
            }
            return client.post(permission_url, json=user_update_payload)

        # Log in
        response = login_user(client, login_url, "test@test.com", "testpassword")
        assert response.status_code == 200
        assert response.json.get("status") == "success"

        # Check permission
        check_response = post_permission_check()
        assert check_response.status_code == 200
        assert check_response.json.get("status") == "success"


# Test the 'remove' permission functionality
def test_permission_remove(client, app, endpoint, port):
    login_url = f"http://localhost:{port}{endpoint}user/login"
    permission_url = f"http://localhost:{port}{endpoint}user/permission"

    with app.app_context():
        def post_permission_remove():
            user_update_payload = {
                "to_id": 1,
                "permission_name": PermissionType.ACCESS_ALL_FLIGHTS,
                "action": "remove",
                "debug_bypass": True
            }
            return client.post(permission_url, json=user_update_payload)

        # Log in
        response = login_user(client, login_url, "test@test.com", "testpassword")
        assert response.status_code == 200
        assert response.json.get("status") == "success"

        # Remove permission
        delete_response = post_permission_remove()
        assert delete_response.status_code == 200
        assert delete_response.json.get("status") == "success"


def test_update_user_info(client, app, endpoint, port):
    # First, register a new user and log them in
    with app.app_context():
        login_url = f"http://localhost:{port}{endpoint}user/login"

        # Login as user 1
        login_response = login_user(client, login_url, "test@test.com", "testpassword")
        assert login_response.status_code == 200
        assert login_response.json.get("status") == "success"

        # Perform update as user 1
        update_url = f"http://localhost:{port}{endpoint}user/update"
        update_data = {"user_username": "josh"}

        update_response = client.post(update_url, data=update_data)

        assert update_response.status_code == 200
        assert update_response.json.get("status") == "success"
        assert update_response.json.get("message") == "Info update successful"
