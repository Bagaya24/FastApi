from fastapi import FastAPI
from typing_extensions import Optional

"""
Dans cette partie que c'est possible de passer directement de arguments dans la fonction sans etre oblige de le mettre sur
la route comme on l'a fait precedement, si on veut que ces arguments soient obligatoire, il faut juste les declaree
sans mettre de valeur par defaut, on se contente souvent d'indiquer juste le type mais si on met une valeur par defaut
alors ce argument de seront pas obligatoires mais optionel, on peut le faire en donnant un valeur par defaut
ou de cette maniere 'Optional[str] = None' ou 'str | None = None', la on dit que l'argument sera soit null soit une
chaine de caracteres, pour le booleen, le module pydentic nous aide de telle maniere que si l'utilisateur tape
'on, off, 1, 0, yes, no' ca convertie ca en True ou False pour nous automatiquement. Voici un exemple d'une route 
ou il y'a a la fois des argument dans la route et sur la fonction 'http://127.0.0.1:3000/users/1/items/hello?q=good%20&short=false'
"""


app = FastAPI()

fake_items_db = [
    {"item_name": "foo"},
    {"item_name": "bar"},
    {"item_name": "baz"}
]

@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

@app.get("/items/{item_id}")
async def get_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "lorem"})
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def get_user_id(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "lorem"})
    return item

