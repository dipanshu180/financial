from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.db.models import Transactions
from src.error import AnalyticsDataNotFound

class AnalyticsService:

    async def get_summary(self, session: AsyncSession):
        query = select(Transactions)
        result = await session.execute(query)
        transactions = result.scalars().all()
        if not transactions:
            raise AnalyticsDataNotFound()

        total_income = sum(tx.amount for tx in transactions if tx.type.lower() == "income")
        total_expense = sum(tx.amount for tx in transactions if tx.type.lower() == "expense")

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": total_income - total_expense
        }

    async def get_category_breakdown(self, session: AsyncSession):
        query = select(Transactions)
        result = await session.execute(query)
        transactions = result.scalars().all()
        if not transactions:
            raise AnalyticsDataNotFound()

        expenses_by_category = {}
        income_by_category = {}

        for tx in transactions:
            if tx.type.lower() == "income":
                income_by_category[tx.category] = income_by_category.get(tx.category, 0.0) + tx.amount
            elif tx.type.lower() == "expense":
                expenses_by_category[tx.category] = expenses_by_category.get(tx.category, 0.0) + tx.amount

        return {
            "expenses_by_category": expenses_by_category,
            "income_by_category": income_by_category
        }

    async def get_monthly_totals(self, session: AsyncSession):
        query = select(Transactions).order_by(Transactions.created_at)
        result = await session.execute(query)
        transactions = result.scalars().all()
        if not transactions:
            raise AnalyticsDataNotFound()

        monthly_totals = {}

        for tx in transactions:
            month_key = tx.created_at.strftime("%Y-%m")
            if month_key not in monthly_totals:
                monthly_totals[month_key] = {"income": 0.0, "expenses": 0.0}

            if tx.type.lower() == "income":
                monthly_totals[month_key]["income"] += tx.amount
            elif tx.type.lower() == "expense":
                monthly_totals[month_key]["expenses"] += tx.amount

        return {"monthly": monthly_totals}

    async def get_recent(self, session: AsyncSession, limit: int = 5):
        query = select(Transactions).order_by(Transactions.created_at.desc()).limit(limit)
        result = await session.execute(query)
        transactions = result.scalars().all()
        if not transactions:
            raise AnalyticsDataNotFound()

        return {
            "recent_activity": [
                {
                    "id": tx.id,
                    "amount": tx.amount,
                    "type": tx.type,
                    "category": tx.category,
                    "date": tx.created_at
                }
                for tx in transactions
            ]
        }