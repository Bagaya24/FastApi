from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, Field

"""
Dans cette partie on a vue que comme pour les argument dans les routes ou les fonctions, on peut aussi donner des attribus
aux elements qui se trouvent dans un body query, ici on utilise la classe 'Field', a part ca, on a aussi vu que pour la 
classe Body, il y'a une attribu 'embed', qui permet de nommer le body query dans le fichier Json.
"""

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = Field("Hello", max_length=20)

@app.put("/item/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id}
    return results