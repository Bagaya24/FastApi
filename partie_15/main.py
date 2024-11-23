from fastapi import FastAPI, status

"""
Dans cette partie nous avons vu les codes de statues, ces codes peuvent aider a l'utisateur de savoir si l'API reagit
comment en fonction des ce qu'il fait, si on ne connait pas tout les codes de statues, on peut juste import 'status' de
fastapi,la on verra tout les codes possibles
"""
app = FastAPI()

@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": str}

@app.delete("/item/{pk}", status_code=204)
async def create_item(pk: str):
    print(f"pk: {pk}")
    return pk

@app.get("/items/", status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def read_items_redirect():
    return {"Hello": "Word"}