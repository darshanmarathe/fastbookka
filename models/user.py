from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    """Has details about user model"""

    id: int
    username: str
    email: Optional[str] = None
    dob: Optional[datetime] = None
    password: str
    createdAt: Optional[datetime] = None
    lastLoggedin: Optional[datetime] = None


class UserLogin(BaseModel):
    username: str
    password: str

class UserChangePassword(BaseModel):
    username: str
    oldPassword: str
    newPassword: str
