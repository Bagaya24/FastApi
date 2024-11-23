from fastapi import FastAPI
from pydantic import BaseModel
"""
Lorsque vous devez envoyer des données d'un client (par exemple, un navigateur) à votre API, vous les envoyez sous la 
forme d'un corps de requête. Ce corps de requête est constitué des données que le client transmet à l'API pour qu'elle 
puisse traiter la demande. En revanche, un corps de réponse est constitué des données que l'API renvoie au client après 
avoir traité la requête.Il est important de noter que votre API doit presque toujours envoyer un corps de réponse. 
Cependant, les clientsne sont pas tenus d'envoyer des corps de requête à chaque fois. Parfois, ils peuvent simplement 
demander un chemin (une URL), éventuellement avec quelques paramètres de requête, sans envoyer de corps.
En résumé :
Corps de requête : Données envoyées par le client à l'API.
Corps de réponse : Données renvoyées par l'API au client.
Les clients peuvent faire des demandes sans toujours inclure des données dans le corps.
Le corps est reprensete dans notre exemple sous forme d'un classe(Item). Pour le POST, on n'a pas besoin de passer 
d'autres paremetre que le corps de la requete mais pour le PUT, DELETE.., on peut envoyer d'autres paremetrer.

"""
app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: int
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def create_item_with_put(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result