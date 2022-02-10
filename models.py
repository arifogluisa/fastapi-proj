import peewee
from database import db


class User(peewee.Model):
    username = peewee.CharField(unique=True)
    email = peewee.CharField(unique=True, index=True)
    password = peewee.CharField()
    is_active = peewee.BooleanField(default=True)

    class Meta:
        database = db


class Task(peewee.Model):
    ip = peewee.CharField(index=True)
    owner = peewee.ForeignKeyField(User, backref="tasks")

    class Meta:
        database = db
