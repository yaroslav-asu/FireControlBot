from bot.crud.base import CRUDBase
from bot.models.user import User
from bot.schemas.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get(self, db: Session, chat_id: int):
        return db.query(self.model).filter(self.model.chat_id == chat_id).first()


user = CRUDUser(User)
