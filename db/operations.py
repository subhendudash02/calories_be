"""
This file contains all operations required in the database.
"""

import sqlalchemy as db
from db.create import user_table, session_table, expected_calorie_table
from auth.jwt import get_username

engine = db.create_engine("sqlite:///./calories.db")
meta = db.MetaData()

def insert(table_name: db.Table | str, values: dict):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    ins = db.insert(table_name).values(**values)

    with engine.connect() as conn:
        conn.execute(ins)
        conn.commit()

def update(table_name: db.Table | str, value: int, username: str):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    up = db.update(table_name).where(table_name.c.username == username).values(calories=value)

    with engine.connect() as conn:
        conn.execute(up)
        conn.commit()

def exists(table_name: db.Table | str, username: str):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    
    valid_row = db.select(table_name).where(table_name.c.username == username)
    row = None
    with engine.connect() as conn:
        for r in conn.execute(valid_row):
           row = r
    return row

def find_password(username: str) -> str:
    valid_row = db.select(user_table).where(user_table.c.username == username)

    with engine.connect() as conn:
        for r in conn.execute(valid_row):
            hashed_password = r[2]
    
    return hashed_password

def get_token() -> str:
    valid_row = db.select(session_table)

    token = None
    with engine.connect() as conn:
        for r in conn.execute(valid_row):
            token = r[2]
    if not token:
        return None

    return token

def delete_session():
    delete_row = db.delete(session_table)

    with engine.connect() as conn:
        conn.execute(delete_row)
        conn.commit()

def get_current_user():
    session = db.select(session_table)

    token = None
    with engine.connect() as conn:
        for r in conn.execute(session):
            token = r[2]
    
    if not token:
        return None
    
    return get_username(token)

def get_calories_goal(username: str, from_date: str, to_date: str | None):
    if not to_date:
        get_calorie = db.select(expected_calorie_table).where(db.and_(expected_calorie_table.c.username == username, expected_calorie_table.c.date == from_date))
    
    calories = 0
    with engine.connect() as conn:
        for r in conn.execute(get_calorie):
            calories += r[2]
    
    return calories

def count_total_calories(table_name: db.Table | str, from_date: str, to_date: str | None):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    if not to_date:
        total_calories = db.select(table_name).where(db.and_(table_name.c.date == from_date))
    else:
        total_calories = db.select(table_name).where(db.and_(table_name.c.date >= from_date, table_name.c.date <= to_date))

    sum = 0
    with engine.connect() as conn:
        for r in conn.execute(total_calories):
            sum += r[2]
    
    return sum

def get_list(table_name: db.Table | str, from_date: str, to_date: str = None):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    
    if not to_date:
        get_all = db.select(table_name).filter(table_name.c.date == from_date)
    else:
        get_all = db.select(table_name).filter(db.and_(table_name.c.date >= from_date, table_name.c.date <= to_date))
    result = []

    with engine.connect() as conn:
        for r in conn.execute(get_all):
            result.append({
                    "id": r[0],
                    "food_name": r[1],
                    "calories": r[2]
                })
    
    return result

def check_role(user: str = None):
    current_user = user if user else get_current_user()
    row = db.select(user_table).where(user_table.c.username == current_user)
    
    role = 0

    with engine.connect() as conn:
        for r in conn.execute(row):
            if r[4] == "admin":
                role = 2
            elif r[4] == "manager":
                role = 1
    
    return role