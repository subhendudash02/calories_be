from e2e import api_request_context
from playwright.sync_api import Playwright, APIRequestContext
import pytest

def test_signup(
    api_request_context: APIRequestContext
):
    data = {
        "username": "test",
        "name": "test",
        "email": "test@gmail.com",
        "password": "123",
        "role": "admin"
    }
    req = api_request_context.post(f"/auth/signup/", data=data);
    assert req.ok, "user already exists / invalid data"

def test_login(
    api_request_context: APIRequestContext
):
    form = {
        "username": "test",
        "password": "123"
    }
    
    req = api_request_context.post(f"/auth/login/", form=form)

    assert req.ok, "invalid creds"