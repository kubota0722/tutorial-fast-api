# 1-firststep.md
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# 2-pathparameter.md
"""
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return {"item_id": item_id}
"""

"""
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
"""

@app.get("/users/me")
async def read_user_me():
    return {"username": "the current user"}

@app.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}

from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    print(model_name)
    if model_name is ModelName.alexnet:
        return {"model_name": model_name.value, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# 3-queryparameter.md

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

"""
@app.get("/items/")
async def read_item(skip: int = 0, limit: int= 10):
    print(skip, limit)
    return fake_items_db[skip : skip + limit]
"""

from typing import Union

"""
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
"""

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

"""
@app.get("/items/{item_id}")
async def read_user_item_1(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item
"""
    
@app.get("/items/{item_id}")
async def read_user_item_1(
    item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
