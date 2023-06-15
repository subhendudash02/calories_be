"""
This file checks the status whether the user is logged in or not
"""

from db.auth import get_token
from auth.jwt import is_token_valid
from db.auth import delete_session


def is_logged_in() -> bool:
    jwt_token = get_token()
    if not jwt_token:
        return False
    if is_token_valid(jwt_token):
        return True
    delete_session()
    return False
