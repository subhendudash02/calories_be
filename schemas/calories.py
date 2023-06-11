from pydantic import BaseModel

class CalorieData(BaseModel):
    food_name: str
    calories: int

class CalorieResponse(BaseModel):
    payload: dict
    msg: str