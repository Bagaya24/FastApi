from pydantic import BaseModel

class ItemBase(BaseModel):
    """
    Represents the base model for an item with common attributes.

    Attributes
    ----------
    title: str
        The title of the item.
    description: str | None, optional
        The description of the item. Defaults to None.
    """
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    """
    ItemCreate class inherits from ItemBase. This class is used to define the schema for creating a new item. It ensures that all required fields for item creation are included and validated according to the constraints defined in ItemBase.
    """
    pass

class Item(ItemBase):
    """
    class Item(ItemBase):
        """
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    """
    UserBase
    --------

    Attributes
    ----------
    email : str
        The email address associated with the user.
    """
    email: str


class UserCreate(UserBase):
    """
    UserCreate extends the UserBase model to include a password field for user creation.

    Attributes:
        password (str): The password for the user.
    """
    password: str

class User(UserBase):
    """
    User class represents a user in the system and inherits from UserBase.

    Attributes
    ----------
    id : int
        Unique identifier for the user.
    is_active : bool
        Indicates if the user is currently active.
    items : list[Item], optional
        List of items associated with the user, by default an empty list.

    Config class provides configuration settings for the User class.

    Attributes
    ----------
    from_attributes : bool
        Indicates if the configuration is sourced from attributes, by default True.
    """
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        from_attributes = True