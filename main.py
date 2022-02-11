from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi



from crud import get_user_by_email, create_user, create_user_task, get_task
import models
import schemas
from database import db_state_default, db
from schemas import UserBase
from secrets import compare_digest
from hashing import Hasher


db.connect()
db.create_tables([models.User, models.Task])
db.close()


app = FastAPI()


async def reset_db_state():
    db._state._state.set(db_state_default.copy())
    db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()


##########################################################################################################

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_access_token_expires: int = 1800  # 30 minutes



@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


# Standard login endpoint. Will return a fresh access token and a refresh token
@app.post('/api/v1/login')
def login(user: UserBase, Authorize: AuthJWT = Depends()):
    """
    create_access_token supports an optional 'fresh' argument,
    which marks the token as fresh or non-fresh accordingly.
    As we just verified their username and password, we are
    going to mark the token as fresh here.
    """
    db_user = get_user_by_email(email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="A user with this email was not found")
    if not Hasher.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    access_token = Authorize.create_access_token(subject=user.email, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}


@app.post('/api/v1/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    """
    Refresh token endpoint. This will generate a new access token from
    the refresh token, but will mark that access token as non-fresh,
    as we do not actually verify a password in this endpoint.
    """
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user, fresh=False)
    return {"access_token": new_access_token}


##########################################################################################################

@app.post("/api/v1/signup", response_model=schemas.User, dependencies=[Depends(get_db)])
def signup(user: schemas.UserCreate):
    db_user = get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(user=user)


@app.get(
    "/api/v1/user", response_model=schemas.User, dependencies=[Depends(get_db)]
)
def read_user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    db_user = get_user_by_email(email=current_user)
    return db_user



@app.post(
    "/api/v1/task",
    response_model=schemas.Task,
    dependencies=[Depends(get_db)],
)
def create_task(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    db_user = get_user_by_email(email=current_user)
    user_id = db_user.id
    return create_user_task(user_id=user_id)


@app.get("/api/v1/status/{id}", response_model=schemas.Task, dependencies=[Depends(get_db)])
def read_task(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    task = get_task(task_id=id)
    return task


###########################################################################################################




def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPIs for Whelp",
        version="2.5.0",
        description="This schema was made for Whelp",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
