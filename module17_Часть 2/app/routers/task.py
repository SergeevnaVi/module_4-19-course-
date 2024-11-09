from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify


router = APIRouter(prefix='/task', tags=['task'])

@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    # Генерация уникального slug для задачи на основе названия
    task_slug = slugify(create_task.title)

    # Создание новой задачи
    new_task = Task(
        title=create_task.title,
        content=create_task.content,
        priority=create_task.priority,
        user_id=user_id,  # Связываем задачу с пользователем
        slug=task_slug    # Присваиваем уникальный slug
    )

    # Вставка новой задачи в таблицу
    db.add(new_task)
    db.commit()

    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.put('/update/{task_id}')
async def update_task(db: Annotated[Session, Depends(get_db)], update_task:UpdateTask, task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.execute(
        update(Task)
        .where(Task.id == task_id)
        .values(update_task.dict(exclude_unset=True))  # Обновляем только те поля, которые были переданы
    )
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful!'
    }


@router.delete('/delete/{task_id}')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task delete is successful!'
    }
