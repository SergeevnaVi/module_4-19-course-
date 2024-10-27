from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import Annotated, List


app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    age: int


users: List[User] = []


@app.get('/users', response_model=List[User])
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}', response_model=User)
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]) -> User:
    if users:
        new_id = users[-1].id + 1
    else:
        new_id = 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return f'User {new_user} is registered'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example=1)],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]
                      ) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return f'The user {user} is registered'
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user_id(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example=1)]) -> User:
    for index, user in enumerate(users):
        if user.id == user_id:
            return users.pop(index)
    raise HTTPException(status_code=404, detail='User was not found')
