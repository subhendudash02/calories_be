"""
This file contains all operations required in the database.
"""

import sqlalchemy as db
from db import engine, meta
from db.models import expected_calorie_table


# insert into the table with the given values
def insert(table_name: db.Table | str, values: dict):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    ins = db.insert(table_name).values(**values)

    with engine.connect() as conn:
        conn.execute(ins)
        conn.commit()


# update the table based on the given values and the username
def update(table_name: db.Table | str, values: dict, username: str):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    up = db.update(table_name).where(table_name.c.username == username).values(**values)

    with engine.connect() as conn:
        conn.execute(up)
        conn.commit()

def delete(table_name: db.Table | str, username: str = None):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    
    if not username:
        table_name.drop(engine)
    else:
        delete = db.delete(table_name).where(table_name.c.username == username)
    
        with engine.connect() as conn:
            conn.execute(delete)
            conn.commit()

# checks whether the username exists in a table
def exists(table_name: db.Table | str, username: str):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)

    valid_row = db.select(table_name).where(table_name.c.username == username)
    row = None
    with engine.connect() as conn:
        for r in conn.execute(valid_row):
            row = r
    return row


def get_calories_goal(username: str, from_date: str, to_date: str | None):
    if not to_date:
        get_calorie = db.select(expected_calorie_table).where(
            db.and_(
                expected_calorie_table.c.username == username,
                expected_calorie_table.c.date == from_date,
            )
        )
    else:
        get_calorie = db.select(expected_calorie_table).filter(
            db.and_(
                expected_calorie_table.c.username == username,
                expected_calorie_table.c.date >= from_date,
                expected_calorie_table.c.date <= to_date,
            )
        )

    calories = 0
    with engine.connect() as conn:
        for r in conn.execute(get_calorie):
            calories += r[2]

    return calories


def count_total_calories(
    table_name: db.Table | str, from_date: str, to_date: str | None
):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    if not to_date:
        total_calories = db.select(table_name).where(
            db.and_(table_name.c.date == from_date)
        )
    else:
        total_calories = db.select(table_name).where(
            db.and_(table_name.c.date >= from_date, table_name.c.date <= to_date)
        )

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
        get_all = db.select(table_name).filter(
            db.and_(table_name.c.date >= from_date, table_name.c.date <= to_date)
        )
    result = []

    with engine.connect() as conn:
        for r in conn.execute(get_all):
            result.append({"id": r[0], "food_name": r[1], "calories": r[2]})

    return result
