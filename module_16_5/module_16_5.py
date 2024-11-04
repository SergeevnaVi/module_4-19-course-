from fastapi import FastAPI, Body, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')


app = FastAPI()
users = []

class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/')
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})

@app.get('/user/{user_id}')
def get_users(request: Request, user_id: int) -> HTMLResponse:
    user = next((u for u in users if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return templates.TemplateResponse('users.html', {'request': request, 'user': user})

@app.post('/user/{username}/{age}')
def create_user(username: str = Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser'),
                age: int = Path(ge=18, le=120, description='Enter age', example=24)) -> User:
    if users:
        new_id = users[-1].id + 1
    else:
        new_id = 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
def update_user(user_id: int = Path(ge=1, le=100, description='Enter User ID', example=1),
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
def delete_user_id(user_id: int = Path(ge=1, le=100, description='Enter User ID', example=1)) -> User:
    for index, user in enumerate(users):
        if user.id == user_id:
            return users.pop(index)
    raise HTTPException(status_code=404, detail='User was not found')


# python -m uvicorn module_16_5:app