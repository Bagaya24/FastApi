from enum import Enum

from fastapi import FastAPI, status
from fastapi.params import Body
from pydantic import BaseModel

"""
Dans cette partie, nous avons vue comment on peut mieux organiser notre code, separer differentes routes en fonction de 
leur utilitees avec l'attribue 'tags', donner une description de la route avec les attribus 'summary' et 'description',
c'est possible aussi de faire la description directement avec le doctstring. Il peut arriver qu'un route devient ou va
devenier obsolete mais qu'on ne veut pas directement l'effacer mais qu'on veut plutot prevenir aux utilisateurs de notre 
API que ca va bientot disparaitre, dans ce cas, on utilise 'deprecated=True'
"""
app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

class Tags(Enum):
    items = "items"
    users = "users"

@app.post("/items",
          response_model=Item,
          status_code=status.HTTP_201_CREATED,
          tags=[Tags.items],
          summary="Create an item",
          #description="Create an item with all the information: name, description, price, tax, tags"
          response_description="The created item"
          )
async def create_item(item: Item = Body(...,embed=True)):
    """
    Create an item with all the information
    - **name**: each item must have a name
    - **description**: a long description
    - **tax**: if the item doesn't have tax, you can omit this
    """
    return item

@app.get("/items/", tags=[Tags.items])
async def read_items():
    return [{"name": "Foo", "price": 42}]

@app.get("/users/", tags=[Tags.users])
async def read_users():
    return [{"Username": "Mr.Robot"}]

@app.get("/elements/", tags=[Tags.items], deprecated=True)
async def read_elements():
    return {"Item_id": "Foo"}
