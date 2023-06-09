from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.auth import SignUpData, SignUpResponse, LoginResponse
from db.create import user_table, session_table
from auth.password import hash_password, verify_password
from db.operations import insert, find_password
from auth.jwt import create_access_token
from uuid import uuid4

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