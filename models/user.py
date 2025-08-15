from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    """Has details about user model"""

    id: int
    username: str
    email: str
    dob: datetime
    password: str
    createdAt: datetime
    lastLoggedin: datetime
