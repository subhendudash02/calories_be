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

def find_password(username: str) -> str:
    valid_row = db.select(user_table).where(user_table.c.username == username)

    with engine.connect() as conn:
        for r in conn.execute(valid_row):
            hashed_password = r[2]
    
    return hashed_password

def get_token() -> str:
    valid_row = db.select(session_table)

    with engine.connect() as conn:
        for r in conn.execute(valid_row):
            token = r[2]
    
    return token

def delete_session():
    delete_row = db.delete(session_table)

    with engine.connect() as conn:
        conn.execute(delete_row)
        conn.commit()

def get_current_user():
    session = db.select(session_table)

    with engine.connect() as conn:
        for r in conn.execute(session):
            token = r[2]
    
    return get_username(token)

def get_calories_goal(from_date: str, to_date: str | None):
    username = get_current_user()
    if not to_date:
        get_calorie = db.select(expected_calorie_table).where(db.and_(expected_calorie_table.c.username == username, expected_calorie_table.c.date == from_date))
    calories = None
    with engine.connect() as conn:
        for r in conn.execute(get_calorie):
            calories = r[2]
    
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