from fastapi import FastAPI
from fastapi.params import Query
"""
Dans cette partie on voit que se possible qu'un argument puisse avoir certains atributs, on peut preciser le nombre
max ou min, et beaucoup d'autres chose, voir documentation. alias permet de donne une autre valeur au parametre
dans la route. C'est aussi possible de cacher un parametre sur le route avec include_schema=False
"""
app = FastAPI()

@app.get("/items")
async def read_items(q: str = Query(None, min_length=3, title="Simple query string", alias="query")):
    results = {"items": [{"item_id": "food"}, {"item_id": "bar"}]}

    if q:
        results.update({"q": q})
    return results

@app.get("/items_hidden")
async def hidden_query(hidden: str | None = Query(None, include_in_schema=False)):
    if hidden:
        return {"hidden": hidden}
    return {"hidden_query": "Not Found"}