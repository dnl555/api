from fastapi.testclient import TestClient
from api.hello import router

client = TestClient(router)


def test_hello():
    response = client.put(
        "/hello/testuser",
        json={"dateOfBirth": "1986-09-15"},
    )
    assert response.status_code == 204

    response = client.get("/hello/testuser")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, testuser! Your birthday is in 180 day(s)"
    }


def test_hello_birthdate_today():
    from datetime import date

    today_date = date.today().replace(year=1900).strftime("%Y-%m-%d")

    response = client.put(
        "/hello/testuser",
        json={"dateOfBirth": today_date},
    )
    assert response.status_code == 204

    response = client.get("/hello/testuser")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, testuser! Happy birthday!"}


def test_error_unknown_user_hello():
    response = client.get("/hello/unknownuser")
    assert response.status_code == 404
    assert response.json() == {"error_msg": "user not found"}


def test_error_invalid_date_hello():
    response = client.put(
        "/hello/testuser",
        json={"dateOfBirth": "1986-09-15T00:00:00.000Z"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "error_msg": "dateOfBirth is not valid, use the format YYYY-MM-DD"
    }


def test_error_date_in_future_hello():
    response = client.put(
        "/hello/testuser",
        json={"dateOfBirth": "2999-09-15"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "error_msg": "dateOfBirth must be a date before the today date"
    }
