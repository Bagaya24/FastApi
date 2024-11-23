from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, user_id: int):
    """
    :param db: Database session object to interact with the database.
    :type db: Session
    :param user_id: The unique identifier of the user to retrieve.
    :type user_id: int
    :return: User object retrieved from the database, or None if no user is found.
    :rtype: models.User or None
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    :param db: Database session used to run the query
    :param email: Email address to search for in the User table
    :return: User object that matches the given email address
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    :param db: A SQLAlchemy Session object to interact with the database.
    :param skip: An integer representing the number of records to skip; default is 0.
    :param limit: An integer representing the maximum number of records to return; default is 100.
    :return: A list of user records matching the query parameters.
    """
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """
    :param db: The database session used for interacting with the database.
    :param user: The user creation schema containing user details.
    :return: The newly created user record from the database.
    """
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int = 0, limit: int = 100):
    """
    :param db: Database session object
    :param skip: Number of records to skip for pagination
    :param limit: Maximum number of records to return
    :return: List of items from the database
    """
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, items: schemas.ItemCreate, user_id: int):
    """
    :param db: Database session object used to interact with the database.
    :param items: Data required to create a new item, adhering to the ItemCreate schema.
    :param user_id: The ID of the user who owns the item.
    :return: The newly created item object after being added to the database, committed, and refreshed.
    """
    db_item = models.Item(**items.model_dump(), owner_id= user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
