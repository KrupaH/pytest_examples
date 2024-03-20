import uvicorn
from fastapi import FastAPI, Body, Path

from app.api_helpers import make_request, save_to_redis, get_from_redis

fastapi_app = FastAPI()


@fastapi_app.get("/")
async def root():
    return {"message": "Hello World"}


@fastapi_app.get("/get_random_user")
async def get_random_user():
    return make_request()


@fastapi_app.post("/post_random_user")
async def post_random_user(key: str = Body(..., description="key to save in redis"),
                           value: str = Body(..., description="value to save in redis")):
    save_to_redis(key, value)
    return {"message": "success"}


@fastapi_app.get("/get_saved_user/{key}")
async def get_saved_user(key: str = Path(..., description="key to check in redis")):
    return {"message": get_from_redis(key)}


if __name__ == '__main__':  # pragma: no cover --> to skip these lines when evaluating test coverage
    uvicorn.run(fastapi_app, host="0.0.0.0", port=19999)
