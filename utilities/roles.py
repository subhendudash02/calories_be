"""
For simplicity, the roles are defined assosciated with their index:
    user: 0
    manager: 1
    admin: 2
"""

import sqlalchemy as db
from db import engine
from db.models import user_table
from db.auth import get_current_user

roles: list = ["user", "manager", "admin"]


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
