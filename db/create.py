"""
This file contains creation of sqlite database and its necesary tables.
"""

import sqlalchemy as db
from uuid import uuid4

engine = db.create_engine("sqlite:///./calories.db", echo=True)
metadata = db.MetaData()

# User table to store user credentials and its role

user_table = db.Table("user", 
                      metadata, 
                      db.Column("ID", db.String, primary_key=True, unique=True),
                      db.Column("username", db.String, unique=True),
                      db.Column("password", db.String),
                      db.Column("email", db.String),
                      db.Column("role", db.String))

# # Food table to store food items and its calories

# food_table = db.Table("food",
#                         metadata,
#                         db.Column("ID", db.String, primary_key=True, default=uuid4, unique=True),
#                         db.Column("name", db.String, unique=True),
#                         db.Column("calories", db.Integer))

# Session table to store user sessions

session_table = db.Table("sessions", 
                         metadata,
                         db.Column("id", db.Integer, primary_key=True, autoincrement=True),
                         db.Column("username", db.Integer, db.ForeignKey("user.username")),
                         db.Column("jwt_token", db.String, unique=True))

metadata.create_all(engine)