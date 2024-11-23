from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

"""
Dans cette partie, nous avons vu comment on peut transformer une structure de donnees en format json avec 'jsonable_encoder'
et par la on a vue que fastapi ne savait pas differencier PUT et PATCH, c'est que signifie que nous devons le faire nous
meme et pour faire, dans le cas du PATCH, il faut juste preciser 'update_data = item.model_dump(exclude_unset=True) '
la donnee ou on veut changer qlq attribue de cette manierem ca signifie que si on ne modifie pas une de ces attributs,
ca va rester telle quel
"""
app = FastAPI()

fake_db = {}


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 32.1
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 30.2},
    "Bar": {"name": "Bar", "description": "The bartenders", "price": 32.1, "tax": 12.4},
    "Baz": {"name": "Baz", "description": None, "price": 30, "tax": 21.4, "tags": []}
}

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items.get(item_id)

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

@app.patch("/items/{item_id}", response_model=Item)
def patch_item(item_id: str, item: Item):
    stored_item_data = items.get(item_id)
    if stored_item_data is not None:
        stored_item_model = Item(**stored_item_data)
    else:
        stored_item_model = Item()
    update_data = item.model_dump(exclude_unset=True)
    update_item = stored_item_model.model_copy(update=update_data)
    items[item_id] = jsonable_encoder(update_item)
    print(items[item_id])
    return update_item