from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI()
users = []

class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def create_user(username: str = Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser'),
                age: int = Path(ge=18, le=120, description='Enter age', example=24)) -> User:
    if users:
        new_id = users[-1].id + 1
    else:
        new_id = 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int = Path(ge=1, le=100, description='Enter User ID', example=1),
                      username: str = Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser'),
                      age: int = Path(ge=18, le=120, description='Enter age', example=24)
                      ) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user_id(user_id: int = Path(ge=1, le=100, description='Enter User ID', example=1)) -> User:
    for index, user in enumerate(users):
        if user.id == user_id:
            return users.pop(index)
    raise HTTPException(status_code=404, detail='User was not found')
