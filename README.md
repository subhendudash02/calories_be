# Calories API

A rest API to manage calories consumed by users, written in Python.

## 🪛 Libraries / Tools Used
- [FastAPI](fastapi.tiangolo.com/) - for creating REST APIs
- SQLite - for storing user data and login sessions
- Pytest - for unit testing
- Black and flake8 - for linting

## Features

1. User can register and login.
2. User can add and delete the calories consumed by him/her.
3. Daily calorie goal can be set by the user and can regularly monitor them.
4. User can also view the calories consumed by him/her in a particular date range.
5. Admins and user managers can control other user's calorie data and their daily goals.

## Roles

There are three roles
- **User**: Users can enter their own calorie data and view them. Not allowed to view or edit any other user's data.

- **User Manager**: User manager or simply *manager* can view and edit any user's calorie data. They can also view and edit any user's daily calorie goal.

- **Admin**: Admins can do everything that a manager can do along with the priviledge of removing any user's / manager's data.

*Note*: For simplicity, the roles are depicted by integers. 0 stands for user, 1 for manager, 2 for admin. Refer `utilities/roles` for more.

# Database

- `user`: stores athe user data with the following fields
    - `ID`: unique UUID for each user
    - `username`: username of the user
    - `password`: hashed password of the user
    - `email`: email of the user
    - `role`: role of the user (user, manager, admin)

- `sessions`: stores the session with the following fields
    - `id`: unique id of the session
    - `jwt_token`: jwt token of the session
    - `username`: user signed in

- `expected_calories`: stores the daily calorie goal of the user with the following fields
    - `ID`: unique id of the goal
    - `username`: username of the user
    - `calories`: daily calorie goal of the user
    - `date`: date of the goal

- `<username>_calorie`: stores the list of food consumed along with the date and time with the following fields
    - `ID`: unique id of the food
    - `food_name`: name of the food
    - `calories`: calories of the food
    - `date`: date when the food was consumed
    - `time`: time when the food was consumed

This table is created after signing up.

## API Endpoints

| Resource | POST | GET | DELETE |
| ----------- | ----------- | ----------- | ----------- |
| `/auth/signup/` | Create a new user with any of the following roles - `user`, `manager`, `admin` | - | - |
| `/auth/login/` | Login with `username` and `password` | - | - |
| `/auth/logout/` | Logs out and deletes the session | - | - |
| `/calories/entry/` | Enter a new food with valid calorie. If calorie is not provided, the calorie is automatically taken from the nutritionix api. | - | - |
| `/calories/entry/{food-id}?username={username}` | - | - | Deletes the food entered before with `food-id` belonging to `username`(optional) |
| `/calories/list?username={username}&from_date={from_date}&to_date={to_date}` | - | Get the list of food consumed from `from_date` to `to_date` by `username`. All the params are optional, by-default the list is shown on daily basis by looged-in user.  | - |
| `/calories/goal/` | sets the calorie goal for the day. | - | - |
| `/calories/goal?username={username}&from_date={from_date}&to_date={to_date}&params=status` | - | Shows the calorie goal summed up from `from-date` to `to-date` of `username`. `params=status` just shows whether you have fulfilled the goal or not. | - |
| `/admin/delete/{username}` | - | - | Removes the user data (Admin only) | 

## 🚀 Installation

- Clone this repository
- Install all the libraries / dependencies

```bash
pip install -r requirements.txt
```

- Rename the file `secrets.demo.cfg` to `secrets.cfg` and enter the required values.

*Note*: 
1. To generate the secret key to encode the JWT token, execute the following command and paste it in the config file.

```bash
openssl rand -hex 32
```

2. To get the nutritionix api key, create an account in [nutritionix](https://www.nutritionix.com/) and get the api key from the [developer portal](https://developer.nutritionix.com/).
**Don't exclose the keys in single/double quotes in config file**

- Run the server, the api will be live in `https://localhost:8000/`

```bash
uvicorn main:app --reload
```

## Directory

<details>
<summary>The directory looks like</summary>

```
├── auth : contains jwt and password related operations
│   ├── __init__.py
│   ├── jwt.py
│   ├── password.py
│   └── status.py
├── calories.db : main db file
├── db : contains all database related operations
│   ├── auth.py
│   ├── __init__.py
│   ├── models.py
│   ├── operations.p
├── main.py : contains fastAPI endpoints
├── README.md
├── requirements.txt
├── routes : contains all the routes
│   ├── admin.py
│   ├── auth.py
│   ├── calories.py
├── schemas : schemas defined for response and request type
│   ├── auth.py
│   ├── calories.py
│   ├── __init__.py
├── secrets.cfg : config file for jwt and nutritionix api key
├── tests : testing environment
│   ├── e2e
│   │   └── demo.py
│   └── unit
│       ├── test_jwt_operations.py
│       ├── test_password_operations.py
│       └── test_table_operations.py
└── utilities : other miscellaneous functions
    ├── check_goal.py
    ├── current_date_time.py
    ├── get_calories.py
    ├── __init__.py
    └── roles.py
```

</details>


## 🧪 Testing

- To run all the unit tests, run the following command

```bash
python -m pytest tests/unit
```

- All the tests are written with the convention `test_<function_name>.py` and the functions as `test_<function_name>`.

- Unit tests are inside `unit/` directory and e2e tests are inside `e2e/` directory. 

## References

- [For authentication](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [For writing basic unit tests](https://www.freecodecamp.org/news/how-to-write-unit-tests-for-python-functions/)
- [Had a hard time figuring out why nutritionix api is not working](https://stackoverflow.com/questions/76465149/getting-401-unauthorized-status-in-an-api)
- [Used SQLAlchemy for the first time](https://docs.sqlalchemy.org/en/20/)