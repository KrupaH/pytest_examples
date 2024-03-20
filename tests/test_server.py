def test_ping(test_client):
    route = "/"
    response = test_client.get(route)
    assert response.json() == {"message": "Hello World"}


def test_get_random_user(test_client):
    route = "/get_random_user"
    response = test_client.get(route)
    assert response.json()["results"]


def test_post_random_user(test_client, sample_user_id):
    sample_value = "test_value"
    route = "/post_random_user"
    response = test_client.post(route, json={"key": sample_user_id, "value": sample_value})
    assert response.json() == {"message": "success"}


def test_get_saved_user(test_client, sample_user_id):
    route = f"/get_saved_user/{sample_user_id}"
    response = test_client.get(route)
    assert response.json() == {"message": "test_value"}  # value set in previous test
