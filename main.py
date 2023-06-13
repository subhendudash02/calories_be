from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from routes import auth, calories

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def sayHello():
    return {"msg": "Hello World"}

app.include_router(auth.auth_router)
app.include_router(calories.cal_router)
