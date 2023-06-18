import auth.jwt as aj


payload = {"sub": "test_user"}


def test_jwt_creation():
    token = aj.create_access_token(payload)
    assert aj.is_token_valid(token) == True
