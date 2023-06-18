import sqlalchemy as sa
from db.models import create_calorie_table
from db.operations import delete

engine = sa.create_engine("sqlite:///./calories.db")
inspect = sa.inspect(engine)


def test_create_user_table():
    assert inspect.has_table("user") == True


def test_create_session_table():
    assert inspect.has_table("sessions") == True


def test_create_expected_calories_table():
    assert inspect.has_table("expected_calories") == True


def test_create_calories_table():
    try:
        create_calorie_table("test_calories")
    except sa.exc.OperationalError:
        pass
    assert inspect.has_table("test_calories") == True


def test_delete_table():
    delete("test_calories")
