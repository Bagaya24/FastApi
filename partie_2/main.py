from fastapi import FastAPI
from enum import Enum
"""
Dans cette partie, nous avons vu les urls dynamiques, il suffit de preciser sur la route le nom du parametre entre 
parenthese, puis l'ecrire sous forme d'arguments dans la fonction. Par defaut la parametre est une chaine de caractere.
Mais on peut preciser si ca sera quel type de variable a travers la fonction ou se passer sous forme d'arguments.
Si jamais deux route se ressemble mais qu'il n'ont pas les memes fonction, l'un peut etre statique et l'autre dynamique
comme nos deux route ici, @app.get("/items/{item_id}") et @app.get("/items/me"), si jamais @app.get("/items/me") vient 
apres @app.get("/items/{item_id}") alors on ne va jamais entrer dans @app.get("/items/me"), voila pourque le route
statique doivent venir avant les routes dynamiques.
Pour finir, on peut preciser des noms de parametres par defaut en creer une classe comme on l'a fait ci dessous dans 
@app.get("/foods/{food_name}"), si jamais on entre un nom qu'on a pas preciser dans la classe, on aura une erreur 422.
"""
app = FastAPI()

@app.get("/items/me")
async def read_own_item():
    return {"item_id": "The current user"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    """
    :param item_id: The ID of the item to retrieve. Must be an integer.
    :return: A dictionary containing the item ID.
    """
    return {"item_id": item_id}


class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    meats = "meats"

@app.get("/foods/{food_name}")
async def read_food(food_name: FoodEnum):
    if food_name == FoodEnum.fruits:
        return {"food": food_name, "message": "You are a fruit lover!"}
    elif food_name.value == "vegetables":
        return {"food": food_name, "message": "You are a vegetarian!"}
    elif food_name == FoodEnum.meats:
        return {"food": food_name, "message": "You are a meat lover!"}


