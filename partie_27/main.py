from datetime import timedelta, datetime

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
"""
Dans cette partie, nous avons vu presque la meme chose que la partie precedente a la difference qu'ici, on est entre 
beaucoup plus en profondeur, on a vue comment hasher un mot de passe et comment deplacer de donner des utilisateurs,
tokens, noms, mot de passe sous format hasher JWT puis comment recuper ces donner et les afficher apres alors ete decoder

"""
app = FastAPI()

SECRET_KEY = "thequickbrownfoxjumpsoverthelazydog"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = dict(
    johndoe=dict(
        username="johndoe",
        full_name="John Doe",
        email="johndoe@example.com",
        hashed_password="$2b$12$vfrEI/JjBHbf3/x2MYTTM.B.Tw.lMWW1qvTgRrHZjmG0UFNWOCh66",
        disable=False
    )
)


class Token(BaseModel):
    """
    Represents an authentication token.

    Attributes:
        access_token: A string representing the access token.
        token_type: A string indicating the type of token.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
        class TokenData(BaseModel):
            username: str | None = None

        Represents the data contained within a token.

        Attributes:
        - username (str | None): The username associated with the token. This can be None if no username is provided.

    """
    username: str | None = None


class User(BaseModel):
    """
    User class represents a user in the system.

    Attributes:
        username (str): The username of the user.
        email (str, optional): The email address associated with the user. Defaults to None.
        full_name (str, optional): The full name of the user. Defaults to None.
        disable (bool, optional): Flag to indicate if the user is disabled. Defaults to None.
    """
    username: str
    email: str | None = None
    full_name: str | None = None
    disable: bool | None = None


class UserInDB(User):
    """
        Class representing a User in the database. Inherits from the User class.

        hashed_password: str
            The hashed version of the user's password.
    """
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """
    :param plain_password: The plain text password input by the user.
    :param hashed_password: The hashed password stored in the system.
    :return: Boolean indicating whether the plain text password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    :param password: The plaintext password that needs to be hashed.
    :return: A hashed representation of the provided plaintext password.
    """
    return pwd_context.hash(password)


def get_user(db, username: str):
    """
    :param db: The database dictionary that stores user data.
    :type db: dict
    :param username: The username to search for in the database.
    :type username: str
    :return: A UserInDB object if the username exists in the database, otherwise None.
    :rtype: UserInDB or None
    """
    if username:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    """
    :param fake_db: The database of users for authentication
    :param username: The username of the user attempting to authenticate
    :param password: The current password provided by the user for authentication
    :return: The authenticated user if credentials are valid, otherwise False
    """
    user = get_user(fake_users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    :param data: A dictionary containing the data to encode in the access token.
    :param expires_delta: An optional timedelta object representing the duration until the token expires. If not provided, defaults to 15 minutes.
    :return: A JWT access token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encode_jwt


@app.post("/token", response_model=Token)
async def loging_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    :param form_data: OAuth2PasswordRequestForm containing username and password
    :return: JSON object with access token and token type

    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expire)

    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    :param token: OAuth2 access token provided for authorization
    :return: The user object if the token is valid and user exists

    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    :param current_user: The user object retrieved from the get_current_user dependency.
    :return: The current active user if the user is not disabled.
    """
    if current_user.disable:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user


@app.get("/users/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """
    :param current_user: The currently authenticated and active user.
    :return: The user object corresponding to the currently authenticated user.
    """
    return current_user


@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    """
    :param current_user: The current active user from the dependency injection.
    :return: A list of items owned by the current user.
    """
    return [{"item_id": "Foo", "owner": current_user.username}]
