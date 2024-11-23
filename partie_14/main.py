from typing import Union, Literal

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

"""
Dans cette partie qui est une cotinuite sur la partie precedent, nous avons vu les differents maniere de strucuter les
reponses que nous donne notre API,nous avons vu comment on peut empecher certains element d'etre afficher mais aussi comment
on peut lier plusieur body query de telle maniere que les reponses de notre API soit un peut dynamique, la classe qui 
permet de lier les body query est 'Union' mais aussi pour restraindre a l'utilisateur de ne pas entrer n'importe quelle
valeur, on peut utiliser la classe 'Literal'
"""
app = FastAPI()
class UserBase(BaseModel):
    username: str
    emai: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return f"supersecret {raw_password}"

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("Userin.dict", user_in.model_dump())
    print("User saved.")
    return user_in_db

@app.post("user", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type: str = "Car"

class PlaneItem(BaseItem):
    type: str = "plane"
    size: int

items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {"description": "Music is my aeroplane, it's my aeroplane", "type": "plane", "size": 4}
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: Literal["item1", "item2"]):
    return items[item_id]

class ListItem(BaseModel):
    name: str
    description: str

list_item = [
    {"name": "Foo", "description": "There comes my heros"},
    {"name": "Red", "description": "It's my aeroplane"}
]

@app.get("/list_items/", response_model=list[ListItem])
async def read_items():
    return list_item

@app.get("/arbitrary", response_model=dict[str, float])
async def get_arbitrary():
    return {"foo": 1, "bar": "5"}
