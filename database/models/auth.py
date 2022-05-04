from sqlalchemy import Column, String

from database.session import Base


class UsedTokens(Base):
    __tablename__ = "used_tokens"
    id = Column(String(500), primary_key=True)
