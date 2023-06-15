"""
Routes for all authentication related endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from schemas.calories import *
from schemas.auth import *
from auth.password import *
from db.models import user_table, session_table, create_calorie_table
from db.operations import *
from db.auth import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.jwt import create_access_token
from uuid import uuid4
from utilities.roles import roles

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/signup/",
    response_model=SignUpResponse,
    responses={201: {"model": SignUpResponse}, 400: {"model": ErrorResponse}},
)
def register(item: SignUpData):
    if item.role not in roles:
        raise HTTPException(
            status_code=400, detail="role can be either admin, manager or user"
        )
    if user_exists(user_table, item.username, item.email):
        raise HTTPException(status_code=400, detail="Username/email-id already exists")

    user_data = item.dict()
    user_data["password"] = hash_password(item.password)
    user_data["ID"] = str(uuid4())
    create_calorie_table(item.username + "_calorie")
    insert(user_table, user_data)

    return {
        "username": item.username,
        "email": item.email,
        "role": item.role,
        "msg": "User created successfully",
    }


@auth_router.post("/login/", response_model=LoginResponse | ErrorResponse)
def login(item: OAuth2PasswordRequestForm = Depends()):
    hashed_password = find_password(item.username)

    if verify_password(item.password, hashed_password):
        access_token = create_access_token(data={"sub": item.username})
        insert_row = {"username": item.username, "jwt_token": access_token}
        insert(session_table, insert_row)
        return {"access_token": access_token, "msg": "Logged in"}
    else:
        return {"detail": "Invalid credentials / user doesn't exist"}


@auth_router.post("/logout/")
def logout():
    delete_session()
    return {"msg": "Logged out"}
