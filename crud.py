import models
import schemas
from ip import get_ip


def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


def get_user_by_email(email: str):
    return models.User.filter(models.User.email == email).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def create_user(user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email, password=user.password)
    db_user.save()
    return db_user


def get_task(task_id: int):
    return models.Task.filter(models.Task.id == task_id).first()


def create_user_task(user_id: int):
    db_task = models.Task(ip=get_ip(), owner_id=user_id)
    db_task.save()
    return db_task
