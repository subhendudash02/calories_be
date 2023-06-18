# Calories API

A rest API to manage calories consumed by users, written in Python.

# Contents
- [Libraries/Tools used](#🪛-libraries--tools-used)
- [Features](#🌟-features)
- [Roles](#💁‍♂️-roles)
- [Database](#📊-database)
- [API Endpoints](#💻-api-endpoints)
- [Core Calories Logic](#🧠-core-calories-logic)
- [Installation](#🚀-installation)
- [Directory](#📃-directory)
- [Testing](#🧪-testing)
- [References](#references)

## 🪛 Libraries / Tools Used
- [FastAPI](fastapi.tiangolo.com/) - for creating REST APIs
- SQLite - for storing user data and login sessions
- [Pytest](https://pytest.org) and [Playwright](https://playwright.dev/) - for testing
- Black - for reformatting

## 🌟 Features

1. User can register and login.
2. User can add and delete the calories consumed by him/her.
3. Daily calorie goal can be set by the user and can regularly monitor them.
4. User can also view the calories consumed by him/her in a particular date range.
5. Admins and user managers can control other user's calorie data and their daily goals.

## 💁‍♂️ Roles

There are three roles
- **User**: Users can enter their own calorie data and view them. Not allowed to view or edit any other user's data.

- **User Manager**: User manager or simply *manager* can view and edit any user's calorie data. They can also view and edit any user's daily calorie goal.

- **Admin**: Admins can do everything that a manager can do along with the priviledge of removing any user's / manager's data.

*Note*: For simplicity, the roles are depicted by integers. 0 stands for user, 1 for manager, 2 for admin. Refer `utilities/roles` for more.

## 📊 Database

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

## 💻 API Endpoints

| Resource | POST | GET | DELETE |
| ----------- | ----------- | ----------- | ----------- |
| `/auth/signup/` | Create a new user with any of the following roles - `user`, `manager`, `admin` | - | - |
| `/auth/login/` | Login with `username` and `password` | - | - |
| `/auth/logout/` | Logs out and deletes the session | - | - |
| `/calories/entry/` | Enter a new food with valid calorie. If calorie is not provided, the calorie is automatically taken from the nutritionix api. | - | Deletes the food entered before with `food-id` belonging to `username`(optional) |
| `/calories/list` | - | Get the list of food consumed from `from_date` to `to_date` by `username`. All the params are optional, by-default the list is shown on daily basis by logged-in user.  | - |
| `/calories/goal/` | sets the calorie goal for the day. | Shows the calorie goal summed up from `from-date` to `to-date` of `username`. `params=status` just shows whether you have fulfilled the goal or not. | - |

*Note*:
- The `username` param / json key is only accessible by the admins and the user managers. That means users can't change or view other's progress.

The request / params model is shown below

1. `/auth/signup/`
 - JSON Request
```
{
    "username": <unique-string>,
    "name": <string>,
    "email": <email>,
    "password": <password>,
    "role": <admin/manager/user>
}
```

- JSON Response
```
{
    "username": <string>,
    "email": <string>,
    "role": <string>,
    "msg": "User created successfully"
}
```

2. `/auth/login/`

- Form body request

| Key | Value |
| ----------- | ----------- |
| username | `string` |
| password | `string` |

- JSON Response
```
{
    "access_token": <JWT-Token>,
    "msg": "Logged in"
}
```

3. `/auth/logout/` - no request body needed

4. `/calories/entry/`

**POST**

- JSON Request
```
{
    "food_name": <string>,
    "calories": <float/integer>
    "username": <string>
}
```

- JSON Response
```
{
    "payload": {
        "food_name": "bacon",
        "calories": 161.46,
        "date": "2023-06-18",
        "time": "11:20:08.909626"
    },
    "msg": "Food entered successfully",
    "goal_reached": null
}
```

**DELETE**
- Params

| Key | Value |
| ----------- | ----------- |
| username | `string` |
| food_id | `integer` |


5. `/calories/goal/`

**GET**
- Params

| Key | Value |
| ----------- | ----------- |
| username | `string` |
| from_date | `date` |
| to_date | `date` |

- JSON Response
```
{
    "msg": 3500
}
```

**POST**
- JSON Request
```
{
    "calories": <int>,
    "username": <string>
}
```

- JSON Response
```
{
    "payload": {
        "username": <string>,
        "calories": 3500,
        "date": "2023-06-18"
    },
    "msg": "Limit set successfully"
}
```

6. `/calories/list/`

**GET**
- Params

| Key | Value |
| ----------- | ----------- |
| username | `string` |
| from_date | `date` |
| to_date | `date` |

- JSON Response
```
{
    "msg": [
        {
            "id": 2,
            "food_name": "bacon",
            "calories": 100
        },
        {
            "id": 3,
            "food_name": "bacon",
            "calories": 100
        },
    ]
}
```

7. `/admin/delete/{username}` - enter the username and POST.

## 🧠 Core Calories Logic

- All the endpoints are authenticated. Users need to create an account and login.
- The name of the food as well as the calories can be mentioned or will be fetched automatically from nutritionix API if not specified. While POSTing the food details, `goal_reached` status will also be shown whether you have reached the goal (true) or not (false). If no daily goal is set, then it will show *null*.
- Goals can be set on a daily basis and the total calorie goals can be shown on a daily basis or for a particular period of days. For example, you can see how much you have set the calorie goal for 5 days cumulative and as well as the `goal_reached` status whether you have reached the goal by summing up those 5 days food data.
- Admins can enter, delete and view other user's and manager's food data and daily goals. Same goes for user managers, but they can't change an admin's data.

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

## 📃 Directory
```
├── auth/
├── db/
├── routes/
├── schemas/
├── tests/
│   ├── e2e/
│   └── unit/
└── utilities/
```

## 🧪 Testing

- Install a dependency for pytest plugin for playwright

```bash
pip install pytest-playwright
```

- To run all the unit tests, run the following command

```bash
python -m pytest tests/
```

- All the tests are written with the convention `test_<function_name>.py` and the functions as `test_<function_name>`.

- Unit tests are inside `unit/` directory and e2e tests are inside `e2e/` directory. 

## References

- [For authentication](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [For writing basic unit tests](https://www.freecodecamp.org/news/how-to-write-unit-tests-for-python-functions/)
- [Had a hard time figuring out why nutritionix api is not working](https://stackoverflow.com/questions/76465149/getting-401-unauthorized-status-in-an-api)
- [Used SQLAlchemy for the first time](https://docs.sqlalchemy.org/en/20/)
- [Got an idea how to write tests in playwright](https://playwright.dev/python/docs/api-testing)