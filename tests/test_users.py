import pytest
from fastapi import status
from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post(
        "/users/",
        json={"email": "hello123@gmail.com", "password": "password123"})

    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post("/login",
                      data={"username": test_user['email'], "password": test_user['password']})

    login_response = schemas.Token(**res.json())
    payload = jwt.decode(login_response.access_token,
                         key=settings.secret_key,
                         algorithms=[settings.algorithm])
    _id = payload.get("user_id")

    assert _id == test_user["id"]
    assert login_response.token_type.lower() == "bearer"
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', status.HTTP_403_FORBIDDEN),
    ('guru@gmail.com', 'wrongpassword', status.HTTP_403_FORBIDDEN),
    ('wrongemail@gmail.com', 'wrongpassword', status.HTTP_403_FORBIDDEN),
    (None, 'password123', status.HTTP_422_UNPROCESSABLE_ENTITY),
    ('guru@gmail.com', None, status.HTTP_422_UNPROCESSABLE_ENTITY)
]

                         )
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login",
                      data={"username": email, "password": password})
    assert res.status_code == status_code
