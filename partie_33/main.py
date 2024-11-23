from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

fake_secret_token = "coneofsilence"
fake_db = dict(
    foo=dict(
        id="foo",
        title="Foo",
        description="There goes my heroes"
    )
)

class Item(BaseModel):
    id: str
    title: str
    description: str | None = None

@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid token")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item no found")
    return fake_db[item_id]

@app.get("/items", response_model=Item)
async def create_item(item: Item, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid token")
    if item in fake_db:
        raise HTTPException(status_code=400, detail="Item already in the database")
    fake_db[item.id] = item
    return item