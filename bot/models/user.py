from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from bot.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    # selected in the menu
    count = Column(Boolean)
    causes = Column(Boolean)
    area = Column(Boolean)
    time = Column(Boolean)

    def __repr__(self):
        return "<User(chat_id='%d')>" % (
            self.chat_id,
        )
