from bot.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()
