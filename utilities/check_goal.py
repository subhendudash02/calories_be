"""
This function will check whether the user has reached the calorie goal or not.
"""

from db.operations import get_calories_goal, count_total_calories


def check_goal(table_name: str, username: str, from_date: str, to_date: str | None):
    todays_goal = get_calories_goal(username, from_date, to_date)
    reached_so_far = count_total_calories(table_name, from_date, to_date)

    if not todays_goal:
        goal_reached = None
    elif todays_goal <= reached_so_far:
        goal_reached = True
    else:
        goal_reached = False

    return goal_reached
