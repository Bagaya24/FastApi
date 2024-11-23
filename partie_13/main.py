from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

"""
Dans cette partie nous avons vue que nous pouvons preciser que que nous voulons a la sortie de notre route par l'attribue
'response',cad que nous pouvons dire a notre route que ca aura comme reponse un body query ou que malgres que ca aura 
comme reponse un body query, que ca puisse exclure ou inclure certains elements. 
"""

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 13.3
    tags: list[str] = []
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "BAr", "description": "The bartenders", "price": 53, "tax": 20.4},
    "baz": {"name": "Baz", "description": None, "price": 40.2, "tax": 13.3, "tags": []}
}

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: Literal["foo", "baz", "bar"]):
    return items[item_id]

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    return item

class UserBase(BaseModel):
    name: str
    full_name: str | None = None
    email: EmailStr

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user

@app.get("/items/{item_id}/name", response_model=Item, response_model_include={"name", "description"})
async def read_item_name(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]

@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_name(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]
