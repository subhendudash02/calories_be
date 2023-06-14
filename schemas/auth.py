"""
This file contains schemas for signup and login and its response models.
"""

from pydantic import BaseModel

# For data creation

class UserData(BaseModel):
    username: str
    email: str
    role: str | None = "user"

class SignUpData(UserData):
    password: str
    
class LoginData(BaseModel):
    username: str
    password: str

# For data response

class SignUpResponse(BaseModel):
    username: str
    email: str
    role: str
    msg: str

class LoginResponse(BaseModel):
    access_token: str
    msg: str
