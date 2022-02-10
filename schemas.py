from typing import Any, List, Optional
import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict
from ip import get_ip


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class TaskBase(BaseModel):
    ip: Optional[str] = None



class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    username: str


class User(BaseModel):
    email: str
    id: int
    is_active: bool
    items: List[Task] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
