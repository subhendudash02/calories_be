"""
This file contains all operations required in the database.
"""

import sqlalchemy as db
from db.create import user_table

engine = db.create_engine("sqlite:///./calories.db", echo=True)

def insert(table_name: db.Table, values: dict):
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