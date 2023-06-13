"""
Routes for inputting calories and daily goals
"""

from fastapi import APIRouter, Depends
from schemas.calories import CalorieData, CalorieResponse, CalorieLimit
from db.create import expected_calorie_table
from db.operations import insert, get_current_user
from auth.status import is_logged_in
from utilities.current_date_time import get_current_date, get_current_time
from datetime import datetime
from utilities.get_calories import *
from utilities.check_goal import check_goal

cal_router = APIRouter(prefix='/calories', tags=['calories'])

@cal_router.post("/entry/")
def enter_food(req: CalorieData, check: bool = Depends(is_logged_in)):
    if not check:
        return {"msg": "Not logged in"}
    else:
        calorie_user_table = get_current_user() + "_calorie"

        calorie_data = req.dict()
        calorie_data['date'] = get_current_date()
        calorie_data['time'] = get_current_time()
        calorie_data["calories"] = get_calories(req.food_name) if not calorie_data["calories"] else calorie_data["calories"]
        insert(calorie_user_table, calorie_data)
        goal_reached = check_goal(calorie_user_table, calorie_data["date"], None)

        return {"payload": calorie_data, "msg": "Food entered successfully", "goal_reached": goal_reached}

@cal_router.post("/set_goal/", response_model=CalorieResponse)
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