from sqlmodel import Field, SQLModel


class UsedTokens(SQLModel, table=True):
    """
    Model for used tokens
    """

    id: str = Field(primary_key=True)
