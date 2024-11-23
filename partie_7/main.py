from fastapi import FastAPI
from fastapi.params import Path, Body
from pydantic import BaseModel

"""
Dans cette partie on a vue qu'on peut avoir plusieur body query sous forme d'argument dans une fonction, il suffit juste
de creer leurs classe mais si jamais on veut creer un simple body query sans qu'on se derange de creer encore une classe
on peut juste le declarer dans le fonction puis utiliser 'Body' qui est comme 'Query' ou 'Path' qu'on a vue precedement
qui nous permet de donner certains attribus a un arguments.
"""

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/items/{item_id}")
async def update_item(
        *,
        item_id: int = Path(..., title="The ID of the item to get", ge=0, le=150),
        q: str | None = None,
        item: Item | None = None,
        user: User,
        importance: int = Body(...)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    if user:
        results.update({"user": user})
    if importance:
        results.update({"importance": importance})
    return results