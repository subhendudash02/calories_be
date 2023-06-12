from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.auth import SignUpData, SignUpResponse, LoginResponse
from schemas.calories import CalorieData, CalorieResponse, CalorieLimit
from db.create import user_table, session_table, create_calorie_table, expected_calorie_table
from auth.password import hash_password, verify_password
from auth.jwt import create_access_token
from db.operations import insert, find_password, get_current_user
from auth.status import is_logged_in
from uuid import uuid4
from utilities.current_date_time import get_current_date, get_current_time
from datetime import datetime
from utilities.get_calories import *

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def sayHello():
    return {"msg": "Hello World"}

@app.post("/signup/", response_model=SignUpResponse)
def register(item: SignUpData):
    user_data = item.dict()
    user_data["password"] = hash_password(item.password)
    user_data["ID"] = str(uuid4())
    create_calorie_table(item.username + "_calorie")
    insert(user_table, user_data)

    return {"username": item.username, "email": item.email, "role": item.role, "msg": "User created successfully"}

@app.post("/login/", response_model=LoginResponse)
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

@app.post("/enter_calorie/", response_model=CalorieResponse)
def enter_food(req: CalorieData, check: bool = Depends(is_logged_in)):
    if not check:
        return {"msg": "Not logged in"}
    else:
        calorie_data = req.dict()
        calorie_data['date'] = get_current_date()
        calorie_data['time'] = get_current_time()
        calorie_data["calories"] = get_calories(req.food_name) if not calorie_data["calories"] else calorie_data["calories"]

        insert(get_current_user() + "_calorie", calorie_data)
        return {"payload": calorie_data, "msg": "Food entered successfully"}

@app.post("/calorie_limit/", response_model=CalorieResponse)
def set_limit(req: CalorieLimit, check: bool = Depends(is_logged_in)):
    if not check:
        return {"msg": "Not logged in"}
    else:
        current_user = get_current_user()
        goal = req.dict()
        goal['date'] = datetime.strptime(req.date, "%d-%m-%y") if req.date else get_current_date()
        goal['username'] = current_user

        insert(expected_calorie_table, goal)
        return {"payload": goal, "msg": "Limit set successfully"}