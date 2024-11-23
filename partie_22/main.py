from fastapi import FastAPI
from fastapi.params import Depends
"""
Dans cette partie, nous avons vue que ca peut arriver que deux routes aient les memes codes, et pour eviter de repeter
les codes, nous pouvons juste creer une fonction qui aura le code et les arguments que les deux routes vont utiliser, 
un peu comme si on creer une classe principale et que les deux routes doivent heriter de ca. Pour se faire, nous 
devons ajouter dans les routes la classe 'Depends'. A noter que la fonction qui a le code de deux routes peut aussi avoir
les codes d'une autre fonction qui a des codes d'autres routes.
"""
app = FastAPI()

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items")
async def read_item(common: dict = Depends(common_parameters)):
    return common


@app.get("/user")
async def read_users(common: dict = Depends(common_parameters)):
    return common
