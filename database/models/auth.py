from sqlmodel import Field, SQLModel


class UsedTokens(SQLModel, table=True):
    id: str = Field(primary_key=True)
