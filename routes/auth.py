"""
Routes for all authentication related endpoints
"""

from fastapi import APIRouter, Depends
from schemas.auth import SignUpData, SignUpResponse, LoginResponse
from auth.password import hash_password, verify_password
from db.create import user_table, session_table, create_calorie_table, expected_calorie_table
from db.operations import insert, find_password, get_current_user, get_calories_goal, count_total_calories
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.jwt import create_access_token
from uuid import uuid4

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.post("/signup/", response_model=SignUpResponse)
def register(item: SignUpData):
    user_data = item.dict()
    user_data["password"] = hash_password(item.password)
    user_data["ID"] = str(uuid4())
    create_calorie_table(item.username + "_calorie")
    insert(user_table, user_data)

    return {"username": item.username, "email": item.email, "role": item.role, "msg": "User created successfully"}

@auth_router.post("/login/", response_model=LoginResponse)
def login(item: OAuth2PasswordRequestForm = Depends()):
    hashed_password = find_password(item.username);

    if verify_password(item.password, hashed_password):
        access_token = create_access_token(
            data={"sub": item.username}
        )
        insert_row = {
            "username": item.username,
            "jwt_token": access_token  
        }
        insert(session_table, insert_row)
        return {"access_token": access_token, "token_type": "bearer", "msg": "Logged in"}
    else:
        return {"msg": "Login failed"}