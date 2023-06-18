from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from routes import auth, calories, admin

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def sayHello():
    return {"msg": "Hello from calories API", "made_by": "Subhendu Dash"}


app.include_router(auth.auth_router)
app.include_router(calories.cal_router)
app.include_router(admin.admin_route)
