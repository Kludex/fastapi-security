from fastapi import FastAPI, HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()


class UserOut(BaseModel):
    username: str


class User(BaseModel):
    username: str
    password: str


database = {
    "users": {
        "sysadmin@sysadmin.com": {
            "username": "sysadmin@sysadmin.com",
            "password": "sysadminfake",
        },
        "test@test.com": {"username": "test@test.com", "password": "test"},
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_hash_password(password: str) -> str:
    return password + "fake"


def create_access_token(username: str) -> str:
    return username


def decode_access_token(token: str) -> str:
    return token


def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    user = database["users"].get(username)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = database["users"].get(form_data.username)
    if user is None:
        raise HTTPException(status_code=403, detail="Incorrect username or password")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user["password"]:
        raise HTTPException(status_code=403, detail="Incorrect username or password")

    access_token = create_access_token(user["username"])
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserOut)
async def read_current_user(user: User = Depends(get_current_user)):
    return user
