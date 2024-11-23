from fastapi import FastAPI
from fastapi.params import Query, Path

"""
Dans cette partie, on fait a peu pres la meme chose que dans la partie precedent mais cette fois ci pour les arguments
qui se trouvent deja sur la route, donc pour des specifications aux arguments qui sont dans la fonction, on utilise
Query et pour ceux qui sont aux routes, on utilise Path
"""

app = FastAPI()

@app.get("/items_validation/{item_id}")
async def read_items_validation(*, item_id: int = Path(..., title="The id of the item", ge=10, le=100), q: str):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})

    return result