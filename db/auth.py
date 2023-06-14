import sqlalchemy as db

engine = db.create_engine("sqlite:///./calories.db")
meta = db.MetaData()

def user_exists(table_name: db.Table | str, username: str, email: str):
    if type(table_name) == str:
        table_name = db.Table(table_name, meta, autoload_with=engine)
    query = db.select(table_name).where(db.or_(table_name.c.username == username, table_name.c.email == email))
    row = None
    with engine.connect() as conn:
        for r in conn.execute(query):
            row = r
    if row:
        return True
    return False