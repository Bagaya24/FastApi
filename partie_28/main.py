import time
from idlelib.debugobj import dispatch

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
"""
Dans cette partie, nous avous vue le Middleware, ca permet d'ajouter des fonctionnalites a une route ou a toute l'app
dans notre exemple ci-desous, nous avons juste augmenter la capacite de pour voir le temps de chargement de la page.
A part le middleware, nous avons aussi vue le CORS, c'est ce qui nous permet de communiquer avec le frontend, c'est un 
peu delicas vue que tu peux y passer la route que tu utilises dans notre cas 'http://localhost:8000/blah' mais ca refuse
d'afficher au front, ca affiche meme une erreur alors qu'au terminal, ca indique que la requete marche donc par
precaution, j'ai mis '*' pour lui signifer que je passe toute les routes,pour le front, nous avons utiliser 'svelte'
mais je pense que nous pouvons utiliser n'importe quel frontend et ca va marcher
"""
app = FastAPI()

class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

origins = [
    "*"]
app.add_middleware(MyMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/blah")
async def blah():
    return {"hello": "world"}