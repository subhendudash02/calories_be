"""
This file contains creation of sqlite database and its necesary tables.
"""

import sqlalchemy as db
from db import engine, meta

# User table to store user credentials and its role

user_table = db.Table(
    "user",
    meta,
    db.Column("ID", db.String, primary_key=True, unique=True),
    db.Column("username", db.String, unique=True),
    db.Column("password", db.String),
    db.Column("email", db.String, unique=True),
    db.Column("role", db.String)
)

# Session table to store user sessions

session_table = db.Table(
    "sessions",
    meta,
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column("username", db.String, db.ForeignKey("user.username")),
    db.Column("jwt_token", db.String, unique=True),
)

# expected_calorie to store expected calorie intake for each user

expected_calorie_table = db.Table(
    "expected_calories",
    meta,
    db.Column("ID", db.Integer, primary_key=True, autoincrement=True),
    db.Column("username", db.String, db.ForeignKey("user.username")),
    db.Column("calories", db.Integer, default=30),
    db.Column("date", db.Date),
)


# table to store food and calorie intake
def create_calorie_table(table_name: str):
    calorie_table = db.Table(
        table_name,
        meta,
        db.Column("ID", db.Integer, primary_key=True, autoincrement=True),
        db.Column("food_name", db.String),
        db.Column("calories", db.Integer),
        db.Column("date", db.Date),
        db.Column("time", db.Time),
        extend_existing=True
    )
    calorie_table.create(engine)


meta.create_all(engine)
