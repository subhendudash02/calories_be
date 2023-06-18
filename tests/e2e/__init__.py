from configparser import ConfigParser
import pytest
from playwright.sync_api import Playwright, APIRequestContext
from typing import Generator

# check for secret key configurations
config = ConfigParser()
config.read("./secrets.cfg")

expire_time = config["jwt"]["ACCESS_TOKEN_EXPIRE_MINUTES"]
secret_key = config["jwt"]["SECRET_KEY"]
x_app_id = config["nutritionix"]["API_ID"]
x_app_key = config["nutritionix"]["API_KEY"]

assert expire_time, "jwt expire time not set"
assert secret_key, "secret key not set"
assert x_app_id, "x_app_id not set"
assert x_app_key, "x_app_key not set"


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(base_url="http://localhost:8000")
    yield request_context
    request_context.dispose()
