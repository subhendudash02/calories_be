import sqlalchemy as db
from db import engine, meta
from db.models import user_table, session_table
from auth.jwt import get_username


def user_exists(table_name: db.Table | str, username: str, email: str):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    query = db.select(table_name).where(
        db.or_(table_name.c.username == username, table_name.c.email == email)
    )
    row = None
    with engine.connect() as conn:
        for r in conn.execute(query):
            row = r
    if row:
        return True
    return False


# get the password of a user
def find_password(username: str) -> str:
    valid_row = db.select(user_table).where(user_table.c.username == username)

    with engine.connect() as conn:
        for r in conn.execute(valid_row):
            hashed_password = r[2]

    return hashed_password


# get jwt token from session table
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
