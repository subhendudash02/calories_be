"""
This file contains schemas for signup and login and its response models.
"""

from pydantic import BaseModel

# For data creation

class SignUpData(BaseModel):
    username: str
    password: str
    email: str
    role: str | None = "user"
    
class LoginData(BaseModel):
    username: str
    password: str

# For data response

class SignUpResponse(BaseModel):
    username: str
    email: str
    role: str
    message: str

class LoginResponse(BaseModel):
    acceess_token: str
    token_type: str
    message: str