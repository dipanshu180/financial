from pydantic import BaseModel
from typing import Dict, List
import uuid
from datetime import datetime

class TransactionSummary(BaseModel):
    id: uuid.UUID
    amount: float
    type: str
    category: str
    date: datetime

class AnalyticsResponse(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float
    expenses_by_category: Dict[str, float]
    income_by_category: Dict[str, float]
    monthly_totals: Dict[str, float]
    recent_activity: List[TransactionSummary]
