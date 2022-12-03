from alembic.config import Config
from alembic import command
from bot.core.config import ROOT

alembic_cfg = Config(ROOT.parent / "alembic.ini")

command.upgrade(alembic_cfg, "head")
