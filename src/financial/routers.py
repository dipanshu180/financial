from fastapi import APIRouter , Depends , status , Query
from src.error import InvalidDateRange, InvalidTransactionType, TransactionNotFound
from .schemas import TransactionCreate , TransactionUpdate
from .services import TransactionService
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer , RoleChecker , get_current_user
from datetime import date
from typing import Optional

services = TransactionService()
access_token_bearer = AccessTokenBearer()
fin_router = APIRouter()

@fin_router.get(
    "/",
    
)
async def get_all_transactions(
    type:       Optional[str]  = Query(None, description="income or expense"),
    category:   Optional[str]  = Query(None, description="e.g. Food, Rent"),
    start_date: Optional[date] = Query(None, description="YYYY-MM-DD"),
    end_date:   Optional[date] = Query(None, description="YYYY-MM-DD"),

    
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
    _:dict= Depends(access_token_bearer),
    role = Depends(RoleChecker(allowed_roles=["admin", "user", "analyst"]))
):
    # validate date range
    if start_date and end_date and start_date > end_date:
        raise InvalidDateRange()

    # validate type if provided
    if type and type not in ["income", "expense"]:
        raise InvalidTransactionType()

    transactions = await services.get_all_transactions(
        session,
        user_id = current_user.id,
        type=type,
        category=category,
        start_date=start_date,
        end_date=end_date
    )

    return {
        "total": len(transactions),
        "transactions": transactions
    }

@fin_router.get("/transactions/{transaction_id}")
async def get_transaction(transaction_id: str , session :AsyncSession  = Depends(get_session),
                          _: dict = Depends(access_token_bearer),
                          current_user = Depends(get_current_user),
                          role = Depends(RoleChecker(allowed_roles=["admin","user","analyst"]))):
    
    transaction = await services.get_transaction_by_id(session , transaction_id)
    if not transaction:
        raise TransactionNotFound()
    return transaction

@fin_router.post("/")
async def create_transaction(user: TransactionCreate , session :AsyncSession = Depends(get_session),
                             _: dict = Depends(access_token_bearer),
                             current_user = Depends(get_current_user),
                             role = Depends(RoleChecker(allowed_roles=["admin"]))):
    
    new_transaction = await services.create_transaction(session , user)
    return new_transaction   
  

@fin_router.patch("/transactions/{transaction_id}")
async def update_transaction(transaction_id: str, transaction_data: TransactionUpdate, session: AsyncSession = Depends(get_session),
                             _: dict = Depends(access_token_bearer),
                             current_user = Depends(get_current_user),
                             role = Depends(RoleChecker(allowed_roles=["admin"]))):
    
    transaction = await services.update_transaction(session, transaction_id, transaction_data)
    if not transaction:
        raise TransactionNotFound()
    return transaction

@fin_router.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: str , session :AsyncSession = Depends(get_session),
                             _: dict = Depends(access_token_bearer),
                             current_user = Depends(get_current_user),
                             role = Depends(RoleChecker(allowed_roles=["admin"]))):
    
    transaction_to_delete = await services.delete_transaction(session , transaction_id)
    if not transaction_to_delete:
        raise TransactionNotFound()
    return {"detail" : "Transaction deleted successfully"}
    
                           
    