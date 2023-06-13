"""
Routes for inputting calories and daily goals
"""

from fastapi import APIRouter, Depends
from schemas.calories import CalorieData, CalorieGoal, CalorieLimit, CalorieResponse
from db.create import expected_calorie_table
from db.operations import *
from auth.status import is_logged_in
from utilities.current_date_time import get_current_date, get_current_time
from datetime import datetime
from utilities.get_calories import *
from utilities.check_goal import check_goal

cal_router = APIRouter(prefix='/calories', tags=['calories'])

@cal_router.post("/entry/", response_model=CalorieResponse)
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

@cal_router.get("/list/")
def list_foods(check: bool = Depends(is_logged_in)):
    if not check:
        return {"msg": "Not logged in"}
    else:
        calorie_user_table = get_current_user() + "_calorie"
        return {"msg": get_list(calorie_user_table)}

@cal_router.post("/goal/")
def set_limit(req: CalorieLimit, check: bool = Depends(is_logged_in)):
    if not check:
        return {"msg": "Not logged in"}
    else:
        current_user = get_current_user()
        goal = req.dict()
        goal['date'] = datetime.strptime(req.date, "%d-%m-%y") if req.date else get_current_date()
        goal['username'] = current_user

        if not exists(expected_calorie_table, current_user):
            insert(expected_calorie_table, goal)
        else:
            update(expected_calorie_table, req.calories, current_user)
        return {"payload": goal, "msg": "Limit set successfully"}

@cal_router.get("/goal/")
def get_limit(check: bool = Depends(is_logged_in)):
    if not check:
        return {"msg": "Not logged in"}
    else:
        current_user = get_current_user()
        res = get_goal(expected_calorie_table, current_user)
        return {"calories": res}