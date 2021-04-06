from typing import List, Optional

from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    name: str
    email: str


class User(BaseUser):
    password: str

    class Config():
        orm_mode = True


class ShowUser(BaseUser):
    class Config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class TopUpData(BaseModel):
    phone: str
    price: int

    class Config():
        orm_mode = True


class SaveTopUp(TopUpData):
    user_id: Optional[int] = Field(..., hidden=True)
