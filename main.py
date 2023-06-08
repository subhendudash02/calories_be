from typing import Union
from fastapi import FastAPI
import sqlalchemy as db
from pydantic import BaseModel
import bcrypt

app = FastAPI()
engine = db.create_engine("sqlite:///./calories.db", echo=True)
metadata = db.MetaData()

class UserData(BaseModel):
    username: str
    password: str
    email: str
    role: str | None = "user"

class LoginData(BaseModel):
    username: str
    password: str

user_table = db.Table("user", 
                      metadata, 
                      db.Column("username", db.String),
                      db.Column("password", db.String),
                      db.Column("email", db.String),
                      db.Column("role", db.String))

metadata.create_all(engine)

# stmt = db.insert(user_table).values(username="subu", password="subu", email="subu@gmail.com", role="admin")
# print(stmt)

# with engine.connect() as conn:
#     result = conn.execute(stmt)
#     conn.commit()

@app.get("/")
def sayHello():
    return {"message": "Hello World"}

@app.post("/signup/")
def register(item: UserData):
    bytes = item.password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    stmt = db.insert(user_table).values(username=item.username, 
                                        password=hash, 
                                        email=item.email, 
                                        role=item.role)
    
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()
        return {"message": "User created successfully"}

@app.post("/login/")
def login(item: LoginData):
    stmt = db.select(user_table).where(user_table.c.username == item.username)
    hashed_password = "";
    with engine.connect() as conn:
        for r in conn.execute(stmt):
            hashed_password = r[1]
    
    if bcrypt.checkpw(item.password.encode("utf-8"), hashed_password):
        return {"message": "Login successful"}
    else:
        return {"message": "Login failed"}