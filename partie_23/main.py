from fastapi import FastAPI, Depends

"""
Dans cette partie, nous avons vue que au lieu de d'utiliser une fonction qui contient un coode commun qui nous retourne
un dictionnaire peut etre limite quand nous voudrons specifier les types, voila pour pourquoi c'est beaucoup mieux 
d'utiliser une classe.
"""
app = FastAPI()

fake_items_db = [
    {"item_name": "foo"},
    {"item_name": "bar"},
    {"item_name": "baz"}
]

class CommonParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(commons=Depends(CommonParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
