from fastapi import FastAPI
"""
Voici un petit code pour creer une application avec FastAPI, tout d'abord on a besoin d'installer fastapi et uvicorn,
uvicorn est le serveur qui permet de lancer une application avec FastAPI, comment on peut le voir, pour creer une 
route GET, il suffit de faire @app.get et ainsi de suite pour les autres routes, pour lancer app, il faut aller 
au terminal et faire la commande uvicorn main:app, main qui est le nom du fichier qui contient l'application et app
est le nom de la variable apres avoir instancie FastAPI, on peut configurer le port ou sera lancer l'application en 
faisant la commande uvicorn main:app --port 8000(par exemple), et pour que notre app puisse se mettre a jour automatiquement
sans qu'on est a redemarer l'app, il faut faire la commande uvicorn main:app --reload.
Il faut noter que FastAPI n'a pas tellement besoin de postman ou un autre logiciel du genre, il suffit d'entre dans
http://127.0.0.1:8000/docs pour voir la documentation de notre application et faire de teste comme on le ferait avec
postman ou un autre logiciel.
"""
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello world"}

@app.post("/")
async def read_root():
    return {"message": "Hello from the post request"}
