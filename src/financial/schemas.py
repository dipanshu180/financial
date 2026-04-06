from pydantic import BaseModel
from enum import Enum

class TransactionType(str, Enum):
    expense = "expense"
    income = "income"


class TransactionCreate(BaseModel):
    amount: float
    type: TransactionType
    category: str
    notes: str


class TransactionUpdate(BaseModel):
    amount: float
    type: TransactionType
    category: str
    notes: str