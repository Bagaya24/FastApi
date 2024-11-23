from fastapi import FastAPI, Form
from fastapi.params import Body
from pydantic import BaseModel

"""
Dans cette partie nous montrons qu'il y'a moyen de recuper les valeur d'un 'form' HTML avec la classe 'Form' et
d'utiliser ces donnees dans notre API mais si nous voulons, c'est aussi possible de directement utiliser le body
query si nous avons fait appel au backend par javascript avec la libraire 'fecth' par exemple
"""
app = FastAPI()


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
class User(BaseModel):
    username: str
    password: str
@app.post("/login-json")
async def login_json(username: str = Body(...), password: str = Body(...)):
    return username