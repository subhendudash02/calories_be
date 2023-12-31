from pydantic import BaseModel
from typing import Any


class CalorieData(BaseModel):
    username: str | None
    food_name: str
    calories: int | None


class CalorieLimit(BaseModel):
    username: str | None
    calories: int
    date: str | None


class CalorieGoal(BaseModel):
    payload: dict
    msg: str


class CalorieResponse(CalorieGoal):
    goal_reached: bool | None


class GetCalorieResponse(BaseModel):
    msg: Any


class ErrorResponse(BaseModel):
    detail: str
