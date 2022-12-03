from pydantic import BaseModel, HttpUrl

from typing import Sequence


class FireBase(BaseModel):
    label: str
    source: str
    url: HttpUrl


class FireCreate(FireBase):
    locality: str

class FireUpdate(FireBase):
    id: int


class FireUpdateRestricted(BaseModel):
    id: int
    label: str


# Properties shared by models stored in DB
class FireInDBBase(FireBase):
    id: int
    submitter_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Fire(FireInDBBase):
    pass


# Properties properties stored in DB
class FireInDB(FireInDBBase):
    pass


class FireSearchResults(BaseModel):
    results: Sequence[Fire]
