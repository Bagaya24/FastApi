from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependacy
def get_db():
    """
    Creates a new database session and ensures that it gets closed after use.

    :return: An active database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/users/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    :param user: An instance of schemas.UserCreate containing user details
    :param db: Database session dependency, provided by FastAPI's Depends
    :return: The created user instance from the database
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    :param skip: The number of records to skip before fetching the users.
    :param limit: The maximum number of users to return.
    :param db: Database session dependency.
    :return: A list of user objects.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    :param user_id: The ID of the user to retrieve.
    :param db: Database session dependency.
    :return: The user object retrieved from the database.

    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int,
                         item: schemas.ItemCreate,
                         db: Session = Depends(get_db)):
    """
    :param user_id: The ID of the user for whom the item is being created.
    :param item: The item data to be created linked to the user.
    :param db: Database session dependency.
    :return: The created item associated with the user.
    """
    return crud.create_user_item(db=db, items=item, user_id=user_id)

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    :param skip: The number of records to skip before starting to return records.
    :param limit: The maximum number of records to return.
    :param db: Database session dependency.
    :return: A list of items retrieved from the database.
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
