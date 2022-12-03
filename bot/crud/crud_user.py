from bot.crud.base import CRUDBase
from bot.models.user import User
from bot.schemas.fire import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass

user = CRUDUser(User)
