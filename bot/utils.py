from bot.db.session import SessionLocal
# gets command that user writes to bot
def command_params_parser(command_text: str) -> list:
    return command_text.split()[1:]

def get_db():
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()
