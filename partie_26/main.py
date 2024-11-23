from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
"""
Ce code Python utilise le framework FastAPI pour créer une API web qui intègre une authentification OAuth2 avec des 
jetons de mots de passe. Voici une explication détaillée de chaque partie du code :
get_user : Récupère les données utilisateur de la base de données fictive.
fake_decode_token : Décode fictivement un jeton d'authentification en un utilisateur.
get_current_user : Récupère l'utilisateur courant basé sur le jeton.
get_current_active_user : Vérifie si l'utilisateur est actif (non désactivé).
/token : Route pour obtenir un jeton d'authentification.
/users/me : Route pour obtenir les informations de l'utilisateur courant.
/items/ : Route pour lire des items, en utilisant le jeton pour l'authentification.
En résumé, ce script utilise FastAPI pour créer une API simple qui comprend l'authentification des utilisateurs via
 OAuth2 et fournit quelques endpoints protégés par cette authentification.
"""
app = FastAPI()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

fake_user_db = {
    "johndoe": dict(
        username="Johndoe",
        full_name="John Doe",
        email="johndoe@exemple.com",
        hashed_password="fakehashedsecret",
        disable=False
    ),
    "alice": dict(
        username= "Alice",
        full_name= "Alice merveille",
        email= "alice@exemple.com",
        hashed_password="fakehashedsecret",
        disable=True

    )
}

def fake_hash_password(password: str):
    return f"fakehashed{password}"



class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disable: bool | None = None

class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    return User(
        username=f"{token} fakedecoded", email="foo@example.com", full_name="Foo bar"
    )

async def get_current_user(token: str = Depends(oauth2_schema)):
    """
    :param token: The token obtained during user authentication
    :return: The decoded user information if the token is valid, otherwise raises an HTTPException with a 401 status code
    """
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    :param current_user: User instance obtained from the dependency injection of get_current_user
    :return: Current active user if the user is not disabled
    :raises HTTPException: If the user is disabled, an HTTP 400 error is raised with the detail "Inactive user"
    """
    if current_user.disable:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    :param form_data: The OAuth2 password request form containing the username and password for authentication.
    :return: A dictionary containing the access token and token type if authentication is successful; raises an HTTPException otherwise.
    """
    user_dict = fake_user_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "Bearer"}


@app.get("/users/me")
async def get_me(current: User = Depends(get_current_active_user)):
    """
    :param current: The current active user obtained from the dependency injection
    :return: The current active user

    """
    return current

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_schema)):
    """
    Endpoint to read items.

    :param token: OAuth2 token provided by the authentication schema.
    :return: JSON response containing the provided token.
    """
    return {"token": token}