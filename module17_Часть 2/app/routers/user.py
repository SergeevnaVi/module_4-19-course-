from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])

@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user

@router.get('/user_id/tasks')
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this user")
    return tasks


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    if not create_user.username:
        raise HTTPException(status_code=400, detail="Username is required")

        # Генерация slug-строки на основе имени пользователя
    user_slug = slugify(create_user.username)

    # Проверка на уникальность slug
    existing_user = db.query(User).filter(User.slug == user_slug).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username is already taken")

    # Создание нового пользователя
    new_user = User(
        username=create_user.username,
        firstname=create_user.firstname,
        lastname=create_user.lastname,
        age=create_user.age,
        slug=user_slug
    )

    # Вставка нового пользователя в таблицу
    db.add(new_user)
    db.commit()

    # Возвращаем успешный статус
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.put('/update/{user_id}')
async def update_user(db: Annotated[Session, Depends(get_db)], update_user:UpdateUser, user_id: int):
    users = db.scalar(select(User).where(User.id == user_id))

    if users is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(
        update(User)
        .where(User.id == user_id)
        .values(update_user.dict(exclude_unset=True))  # Обновляем только те поля, которые были переданы
    )
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }


@router.delete('/delete/{user_id}')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))

    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    # Удаляем все задачи пользователя
    db.execute(delete(Task).where(Task.user_id == user_id))

    # Удаляем пользователя
    db.execute(delete(User).where(User.id == user_id))
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User and associated tasks deleted successfully'
    }
