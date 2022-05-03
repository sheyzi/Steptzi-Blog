from fastapi import Depends

from database.session import Session, get_db
from database.models import UsedTokens


class AuthRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def add_used_token(self, token: str):
        used_token = UsedTokens(id=token)
        self.db.add(used_token)
        self.db.commit()
        return True

    def get_used_token(self, token: str):
        return self.db.query(UsedTokens).get(token)
