from unicodedata import category

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from sqlmodel import select  
from .schemas import TransactionCreate , TransactionUpdate
from src.db.models import Transactions 
from src.error import TransactionNotFound, InvalidAmountValue, EmptyUpdateData
from src.auth.dependencies import get_current_user , RoleChecker , AccessTokenBearer
from typing import Optional
from datetime import date
import uuid

class TransactionService:
    async def get_all_transactions(
    self,
    session:    AsyncSession,
    user_id: uuid.UUID,
    type:       Optional[str]  = None,
    category:   Optional[str]  = None,
    start_date: Optional[date] = None,
    end_date:   Optional[date] = None
):
        query = select(Transactions).where(
        Transactions.user_id == user_id   # 🔥 MAIN FIX
     )

        # apply filters only if provided
        if type:
            query = query.where(Transactions.type == type)
        if category:
            query = query.where(Transactions.category == category)
        if start_date:
            query = query.where(Transactions.date >= start_date)
        if end_date:
            query = query.where(Transactions.date <= end_date)

        result       = await session.execute(query)
        transactions = result.scalars().all()
        return transactions
    
    async def get_transaction_by_id(self , session:AsyncSession , transaction_id : str):
        query = select(Transactions).where(Transactions.id == transaction_id)
        result = await session.execute(query)
        transaction = result.scalars().first()
        return transaction
    
    async def create_transaction(self , session:AsyncSession , transaction_data : TransactionCreate):
        if transaction_data.amount <= 0:
            raise InvalidAmountValue()
        transaction_data_dict = transaction_data.model_dump()
        new_transaction = Transactions(**transaction_data_dict)
        session.add(new_transaction)
        await session.commit()
        await session.refresh(new_transaction)
        return new_transaction
    

    async def delete_transaction(self, session: AsyncSession, transaction_id: str):
        transaction_to_delete = await self.get_transaction_by_id(session, transaction_id)

        if not transaction_to_delete:
            raise TransactionNotFound()

        await session.delete(transaction_to_delete)
        await session.commit()

        return transaction_to_delete  

    async def update_transaction(self , session:AsyncSession , transaction_id : str , transaction_data : TransactionUpdate):
        transaction_to_update = await self.get_transaction_by_id(session , transaction_id)
        if not transaction_to_update:
            raise TransactionNotFound()
        transaction_data_dict = transaction_data.model_dump(exclude_unset=True)
        if not transaction_data_dict:
            raise EmptyUpdateData()
        if "amount" in transaction_data_dict and transaction_data_dict["amount"] <= 0:
            raise InvalidAmountValue()
        for key , value in transaction_data_dict.items():
            setattr(transaction_to_update , key , value)
        session.add(transaction_to_update)
        await session.commit()
        await session.refresh(transaction_to_update)
        return transaction_to_update
    