"""
Routes for inputting calories and daily goals
"""

from fastapi import APIRouter, Depends, HTTPException
from schemas.calories import *
from db.models import expected_calorie_table
from db.operations import *
from db.auth import *
from auth.status import is_logged_in
from utilities.current_date_time import *
from datetime import datetime
from utilities.roles import *
from utilities.get_calories import *
from utilities.check_goal import check_goal

cal_router = APIRouter(prefix="/calories", tags=["calories"])


@cal_router.post(
    "/entry/",
    response_model=CalorieResponse,
    responses={
        201: {"model": CalorieResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
)
def enter_food(
    req: CalorieData,
    check: bool = Depends(is_logged_in),
    role: int = Depends(check_role),
):
    if not check:
        raise HTTPException(status_code=401, detail="Not logged in")
    if role == 1 and check_role(req.username) == 2:
        raise HTTPException(
            status_code=403, detail="user manager can't access admin's records"
        )
    if role == 0 and req.username:
        raise HTTPException(status_code=403, detail="User can't access other records")

    current_user = req.username if req.username else get_current_user()
    calorie_user_table = current_user + "_calorie"
    calorie_data = req.dict()

    calorie_data["date"] = get_current_date()
    calorie_data["time"] = get_current_time()
    calorie_data["calories"] = (
        get_calories(req.food_name)
        if not calorie_data["calories"]
        else calorie_data["calories"]
    )
    calorie_data.pop("username")

    insert(calorie_user_table, calorie_data)
    goal_reached = check_goal(
        calorie_user_table, current_user, calorie_data["date"], None
    )

    return {
        "payload": calorie_data,
        "msg": "Food entered successfully",
        "goal_reached": goal_reached,
    }


@cal_router.delete("/entry/{food_id}", response_model=GetCalorieResponse, responses={
        201: {"model": CalorieResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },)
def delete_food(
    food_id: int,
    username: str = None,
    check: bool = Depends(is_logged_in),
    role: int = Depends(check_role),
):
    if not check:
        raise HTTPException(status_code=401, detail="Not logged in")
    if role == 1 and check_role(username) == 2:
        raise HTTPException(
            status_code=403, detail="user manager can't access admin's records"
        )
    if role == 0 and username:
        raise HTTPException(status_code=403, detail="User can't access other records")

    current_user = username if username else get_current_user()
    calorie_user_table = current_user + "_calorie"

    remove_food(calorie_user_table, food_id)

    return {"msg": "removed successfully"}


@cal_router.get(
    "/list",
    response_model=GetCalorieResponse,
    responses={
        200: {"model": GetCalorieResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
)
def list_foods(
    username: str = None,
    from_date: str = None,
    to_date: str = None,
    check: bool = Depends(is_logged_in),
    role: int = Depends(check_role),
):
    if not check:
        raise HTTPException(status_code=401, detail="Not logged in")
    if role == 1 and check_role(username) == 2:
        raise HTTPException(
            status_code=403, detail="user manager can't access admin's records"
        )
    if role == 0 and username:
        raise HTTPException(status_code=403, detail="User can't access other records")

    current_user = username if username else get_current_user()
    calorie_user_table = current_user + "_calorie"

    if not from_date:
        from_date = get_current_date()

    food_list = get_list(calorie_user_table, from_date, to_date)

    return {"msg": food_list}


@cal_router.post(
    "/goal/",
    response_model=CalorieGoal,
    responses={
        201: {"model": CalorieGoal},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
)
def set_limit(
    req: CalorieLimit,
    check: bool = Depends(is_logged_in),
    role: int = Depends(check_role),
):
    if not check:
        raise HTTPException(status_code=401, detail="Not logged in")
    if role == 1 and check_role(req.username) == 2:
        raise HTTPException(
            status_code=403, detail="user manager can't access admin's records"
        )
    if role == 0 and req.username:
        raise HTTPException(status_code=403, detail="User can't access other records")

    current_user = req.username if req.username else get_current_user()
    goal = req.dict()
    goal["date"] = (
        datetime.strptime(req.date, "%d-%m-%y") if req.date else get_current_date()
    )
    goal["username"] = current_user

    if not exists(expected_calorie_table, current_user):
        insert(expected_calorie_table, goal)
    else:
        update(expected_calorie_table, {"calories": req.calories}, current_user)

    return {"payload": goal, "msg": "Limit set successfully"}


@cal_router.get(
    "/goal",
    response_model=GetCalorieResponse,
    responses={
        200: {"model": GetCalorieResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
)
def get_limit(
    params: str = None,
    username: str = None,
    from_date: str = None,
    to_date: str = None,
    check: bool = Depends(is_logged_in),
    role: int = Depends(check_role),
):
    if not check:
        raise HTTPException(status_code=401, detail="Not logged in")
    if role == 1 and check_role(username) == 2:
        raise HTTPException(
            status_code=403, detail="user manager can't access admin's records"
        )
    if role == 0 and username:
        raise HTTPException(status_code=403, detail="User can't access other records")

    current_user = username if username else get_current_user()

    if not from_date:
        from_date = get_current_date()

    res = get_calories_goal(current_user, from_date, to_date)

    if params == "status":
        res2 = check_goal(current_user + "_calorie", current_user, from_date, to_date)
        return {"msg": res2}

    return {"msg": res}
