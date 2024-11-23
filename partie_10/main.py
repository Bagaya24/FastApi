from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
"""
Dans cette partie, on a essaye de voir comment on peut donner de valeur pas par defaut mais des valeurs qui sont comme
des exemples pour aider l'utilisateur de notre API de pouvoir se retrouver facilement, il y'a trois maniere de faire,
en creer la classe Config, ca n'a pas marche dans mon cas, en precisant le valeur de l'exemple avec l'attribu 'example'
dans la classe Field,qui n'a pas aussi marche dans mon cas et finalement en precisant la valeur de l'exemple dans l'attribu
'example' dans la classe Body pour avoir un seul exemple ou l'attribue 'examples' pour avoir plusieurs exemples
"""
app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    # class Config:
    #     schema_extra = {
    #         "exemple":{
    #             "name": "foo",
    #             "description": "A very good Item",
    #             "price": 14.2,
    #             "tax": 2.14
    #         }
    #
    #     }

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., example=[
    {
            "name": "foo",
            "description": "A very good Item",
            "price": 24.24,
            "tax": 2.13
    },

    {
        "name": "Bar",
        "price": "23.12"
    }

       ])):
    results = {"item_id": item_id, "item": item}
    return results