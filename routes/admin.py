"""
Routes for all admin related stuffs
"""

from fastapi import APIRouter, Depends, HTTPException
from db.operations import *
from auth.status import is_logged_in
from utilities.roles import *
from utilities.get_calories import *
from db.operations import delete

admin_route = APIRouter(prefix="/admin", tags=["admin"])


@admin_route.delete("/delete/{username}")
def delete_user(
    username: str, check: bool = Depends(is_logged_in), role: int = Depends(check_role)
):
    if not check:
        raise HTTPException(status_code=401, detail="Not logged in")
    if role == 1:
        raise HTTPException(
            status_code=400, detail="user manager can't delete user data"
        )
    if role == 0 and username:
        raise HTTPException(
            status_code=400, detail="User can't delete their data. Contact the admin."
        )

    if not exists("user", username):
        raise HTTPException(status_code=400, detail="username doesn't exist")

    delete("user", username)
    delete("expected_calories", username)
    delete(username + "_calorie", None)

    return {"msg": ("deleted user %s" % username)}
