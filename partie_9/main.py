from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, HttpUrl
"""
Dans cette partie on voit que se possible de mettre un body query dans un body query , il faut juste le preciser dans 
un de corps.
"""

app = FastAPI()
class Image(BaseModel):
    url: HttpUrl
    name: str
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    image: Image | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
