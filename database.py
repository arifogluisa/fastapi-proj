import os
from contextvars import ContextVar
import peewee
from dotenv import load_dotenv
load_dotenv()


DATABASE_NAME = "newestdb.db"
db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db = peewee.MySQLDatabase(str(os.getenv('DATABASE_NAME')), user=str(os.getenv('USER_DB')),
                          password=str(os.getenv('PASSWORD_DB')), host=str(os.getenv('HOST_DB')), port=3306)
db._state = PeeweeConnectionState()
