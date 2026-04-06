from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException, RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

# ─────────────────────────────────────────
# BASE EXCEPTION
# ─────────────────────────────────────────

class Finance(Exception):
    """This is the base class for all finance errors"""
    pass


# ─────────────────────────────────────────
# AUTH ERRORS (your existing ones)
# ─────────────────────────────────────────

class InvalidToken(Finance):
    """User has provided an invalid or expired token"""
    pass


class RevokedToken(Finance):
    """User has provided a token that has been revoked"""
    pass


class AccessTokenRequired(Finance):
    """User has provided a refresh token when an access token is needed"""
    pass


class RefreshTokenRequired(Finance):
    """User has provided an access token when a refresh token is needed"""
    pass


class UserAlreadyExists(Finance):
    """User has provided an email for a user who exists during sign up."""
    pass


class InvalidCredentials(Finance):
    """User has provided wrong email or password during log in."""
    pass


class InsufficientPermission(Finance):
    """User does not have the necessary permissions to perform an action."""
    pass


class UserNotFound(Finance):
    """User Not found"""
    pass


class AccountNotVerified(Finance):
    """Account not yet verified"""
    pass


# ─────────────────────────────────────────
# TRANSACTION ERRORS
# ─────────────────────────────────────────

class TransactionNotFound(Finance):
    """Transaction with given ID does not exist"""
    pass


class InvalidTransactionType(Finance):
    """Transaction type must be income or expense"""
    pass


class InvalidAmountValue(Finance):
    """Transaction amount must be greater than 0"""
    pass


class InvalidDateRange(Finance):
    """start_date cannot be after end_date"""
    pass


class EmptyUpdateData(Finance):
    """No fields were provided to update"""
    pass


# ─────────────────────────────────────────
# ANALYTICS ERRORS
# ─────────────────────────────────────────

class InvalidLimitValue(Finance):
    """Limit value is out of allowed range"""
    pass


class AnalyticsDataNotFound(Finance):
    """No transaction data available for analytics"""
    pass


# ─────────────────────────────────────────
# EXCEPTION HANDLER FACTORY
# ─────────────────────────────────────────

def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: Finance):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


# ─────────────────────────────────────────
# REGISTER ALL ERRORS
# ─────────────────────────────────────────

def register_all_errors(app: FastAPI):

    # ── AUTH ──────────────────────────────

    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get a refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account Not verified",
                "error_code": "account_not_verified",
                "resolution": "Please check your email for verification details",
            },
        ),
    )

    # ── TRANSACTION ───────────────────────

    app.add_exception_handler(
        TransactionNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Transaction not found",
                "error_code": "transaction_not_found",
            },
        ),
    )

    app.add_exception_handler(
        InvalidTransactionType,
        create_exception_handler(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            initial_detail={
                "message": "Transaction type must be income or expense",
                "error_code": "invalid_transaction_type",
            },
        ),
    )

    app.add_exception_handler(
        InvalidAmountValue,
        create_exception_handler(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            initial_detail={
                "message": "Amount must be greater than 0",
                "error_code": "invalid_amount_value",
            },
        ),
    )

    app.add_exception_handler(
        InvalidDateRange,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "start_date cannot be after end_date",
                "error_code": "invalid_date_range",
            },
        ),
    )

    app.add_exception_handler(
        EmptyUpdateData,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "No fields provided to update",
                "error_code": "empty_update_data",
            },
        ),
    )

    # ── ANALYTICS ─────────────────────────

    app.add_exception_handler(
        InvalidLimitValue,
        create_exception_handler(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            initial_detail={
                "message": "Limit must be between 1 and 20",
                "error_code": "invalid_limit_value",
            },
        ),
    )

    app.add_exception_handler(
        AnalyticsDataNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "No transaction data available for analytics",
                "error_code": "analytics_data_not_found",
            },
        ),
    )

    # ── GLOBAL ────────────────────────────

    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            content={
                "message": exc.detail,
                "error_code": "error",
            },
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            content={
                "message": "Validation Error",
                "error_code": "validation_error",
                "errors": exc.errors(),
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )