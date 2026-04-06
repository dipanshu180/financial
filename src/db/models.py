from sqlmodel import SQLModel, Field , Column , Relationship
import uuid
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime , date 
import sqlalchemy as sa
from src.financial.schemas import TransactionType
from typing import List
from sqlalchemy import Enum
from sqlalchemy import ForeignKey

class User(SQLModel,table=True):
    __tablename__ = "users"
    id : uuid.UUID = Field(sa_column = Column(pg.UUID(as_uuid = True), primary_key = True , default = uuid.uuid4))
    name : str 
    email : str
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )
    role : str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    is_verified :bool = Field(default=False)
    transactions: List["Transactions"] = Relationship(
        back_populates="user"
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


class Transactions(SQLModel , table = True):
    __tablename__ = "transactions"
    id : uuid.UUID = Field(sa_column = Column(pg.UUID(as_uuid = True), primary_key = True , default = uuid.uuid4))
    amount : float
    type: TransactionType = Field(
    sa_column=Column(
        Enum(TransactionType, name="transactiontype", create_type=False)
    )
)
    user_id: uuid.UUID = Field(
    sa_column=Column(
        pg.UUID(as_uuid=True),
        ForeignKey("users.id"),   
        nullable=False
    )
)
    category : str
    notes : str
    user: "User" = Relationship(back_populates="transactions")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))