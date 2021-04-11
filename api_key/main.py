import secrets
from typing import List

from fastapi import FastAPI, HTTPException, Security
from fastapi.param_functions import Depends, Query
from fastapi.security import APIKeyHeader, SecurityScopes
from pydantic import BaseModel

app = FastAPI()

api_key_header_auth = APIKeyHeader(name="X-API-KEY", auto_error=False)


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
            "api_keys": [],
        },
        "test@test.com": {
            "username": "test@test.com",
            "password": "test",
            "api_keys": [],
        },
    }
}


def get_current_user():
    return database["users"]["sysadmin@sysadmin.com"]


async def get_api_key(
    security_scopes: SecurityScopes, api_key_header: str = Security(api_key_header_auth)
):
    for user in database["users"].values():
        for api_key in user["api_keys"]:
            if int(api_key["key"]) == int(api_key_header) and set(
                api_key["scopes"]
            ) <= set(security_scopes.scopes):
                return "Authenticated"
    raise HTTPException(status_code=403, detail="Not authenticated")


@app.post("/api-key")
async def generate_api_key(
    scopes: List[str] = Query(...), user: User = Depends(get_current_user)
):
    key = secrets.randbits(10)
    username = user["username"]
    database["users"][username]["api_keys"].append({"key": key, "scopes": scopes})
    return key


@app.get("/users/me", dependencies=[Security(get_api_key, scopes=["users"])])
async def read_current_user():
    return "Hello world!"
