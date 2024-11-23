from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    """
    Defines the User model, used to represent users within the application.

    Class Attributes:
        __tablename__ (str): The name of the table in the database.
        id (Column): The primary key of the user table. Indexed for fast search.
        email (Column): The email address of the user. Must be unique and is indexed.
        hashed_password (Column): The hashed password of the user.
        is_active (Column): A boolean indicating whether the user is active. Defaults to True.
        items (relationship): The relationship to items owned by the user.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # index permet de chercher un element dans la base de donnees
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    """
        SQLAlchemy Item Model

        Represents an item in the database.

        Attributes:
        - __tablename__: str
            The name of the table in the database.

        - id: Column
            The primary key of the item.

        - title: Column
            The title of the item.

        - description: Column
            The description of the item.

        - owner_id: Column
            The foreign key referencing the owning user.

        - owner: relationship
            The relationship to the User model, indicating the owner of the item.
    """
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")