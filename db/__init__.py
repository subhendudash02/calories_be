import sqlalchemy as db

engine = db.create_engine("sqlite:///./calories.db")
meta = db.MetaData()