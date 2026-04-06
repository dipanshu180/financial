from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from .services import AnalyticsService
from src.auth.dependencies import RoleChecker, AccessTokenBearer
from src.error import InvalidLimitValue

analytic_router = APIRouter(prefix="/analytics", tags=["Analytics"])
services = AnalyticsService()

@analytic_router.get("/summary")
async def get_summary(
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(AccessTokenBearer()),
    current_user = Depends(RoleChecker(allowed_roles=[ "analyst", "admin"]))
):
    return await services.get_summary(session)

@analytic_router.get("/by-category")
async def get_by_category(
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(AccessTokenBearer()),
    current_user = Depends(RoleChecker(allowed_roles=[ "analyst", "admin"]))
):
    return await services.get_category_breakdown(session)

@analytic_router.get("/monthly")
async def get_monthly(
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(AccessTokenBearer()),
    current_user = Depends(RoleChecker(allowed_roles=["analyst", "admin"]))
):
    return await services.get_monthly_totals(session)

@analytic_router.get("/recent")
async def get_recent(
    limit: int = Query(default=5, le=20),
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(AccessTokenBearer()),
    current_user = Depends(RoleChecker(allowed_roles=["analyst", "admin"]))
):
    if limit < 1 or limit > 20:
        raise InvalidLimitValue()
    return await services.get_recent(session, limit)