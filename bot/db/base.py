# Import all the models, so that Base has them before being
# imported by Alembic
from bot.db.base_class import Base  # noqa
from bot.models.user import User  # noqa
