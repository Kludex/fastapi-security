import secrets

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security.http import HTTPBasic, HTTPBasicCredentials
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
            "password": "sysadmin",
        },
        "test@test.com": {"username": "test@test.com", "password": "test"},
    }
}

security = HTTPBasic()


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = database["users"].get(credentials.username)
    if user and secrets.compare_digest(credentials.password, user["password"]):
        return user
    raise HTTPException(
        status_code=401,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Basic"},
    )


@app.get("/users/me", response_model=UserOut)
async def read_current_user(user: User = Depends(get_current_user)):
    return user
