from e2e import api_request_context
from playwright.sync_api import Playwright, APIRequestContext


def test_add_food(api_request_context: APIRequestContext):
    data = {"food_name": "1 cup biriyani", "username": "test"}
    req = api_request_context.post(f"/calories/entry/", data=data)
    assert req.ok, "invalid data"


def test_add_goal(api_request_context: APIRequestContext):
    data = {"calories": 2300, "username": "test"}
    req = api_request_context.post(f"/calories/goal/", data=data)
    assert req.ok, "invalid data"


def test_add_more_food(api_request_context: APIRequestContext):
    data = {"food_name": "1 cup biriyani", "username": "test"}
    req = api_request_context.post(f"/calories/entry/", data=data)
    body = req.json()
    assert body["goal_reached"] == False
