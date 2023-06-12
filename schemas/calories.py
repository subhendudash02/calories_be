from pydantic import BaseModel

class CalorieData(BaseModel):
    food_name: str
    calories: int | None

class CalorieLimit(BaseModel):
    calories: int
    date: str | None
    
class CalorieResponse(BaseModel):
    payload: dict
    msg: str
