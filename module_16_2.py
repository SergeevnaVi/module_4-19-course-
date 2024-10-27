from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

@app.get("/")
async def welcome():
    return "Главная страница"

@app.get("/user/admin")
async def admin():
    return "Вы вошли как администратор"

@app.get("/user/{username}/{age}")
async def user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]):
    return f'Информация о пользователе. Имя: {username}, Возраст: {age}'

@app.get("/user/{user_id}")
async def user_id(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example=1)]):
    return f"Вы вошли как пользователь №{user_id}"

