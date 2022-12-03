from bot.crud.base import CRUDBase
from bot.models.fire import Fire
from bot.schemas.fire import FireCreate, FireUpdate


class CRUDFire(CRUDBase[Fire, FireCreate, FireUpdate]):
    pass

fire = CRUDFire(Fire)
