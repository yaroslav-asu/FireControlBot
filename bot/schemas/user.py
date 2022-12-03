from pydantic import BaseModel

from typing import Sequence


class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    chat_id: int
    count: bool = False
    causes: bool = False
    area: bool = False
    time: bool = False

class UserUpdate(UserBase):
    id: int
    count: bool
    causes: bool
    area: bool
    time: bool


class UserUpdateRestricted(BaseModel):
    id: int

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Fire(UserInDBBase):
    pass


# Properties properties stored in DB
class FireInDB(UserInDBBase):
    pass


class UserSearchResults(BaseModel):
    results: Sequence[Fire]
