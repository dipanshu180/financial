from fastapi import APIRouter , Depends , status, HTTPException
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas import UserCreate , UserModel , UserLoginModel
from src.auth.services import UserService 
from .utils import verify_password , create_access_token
from datetime import datetime
from datetime import timedelta
from fastapi.responses import JSONResponse
from .dependencies import AccessTokenBearer , RefreshTokenBearer , get_current_user , RoleChecker
from src.config import config
from src.db.redis import add_jti_to_blocklist
from src.error import UserAlreadyExists, UserNotFound, InvalidCredentials, InvalidToken

auth_router = APIRouter()

REFRESH_TOKEN_EXPIRY = 7
role_checker = RoleChecker(allowed_roles=["admin","user"])
services = UserService()

@auth_router.post("/signup" , status_code = status.HTTP_201_CREATED )
async def signup(user: UserCreate , session: AsyncSession = Depends(get_session)):
    email = user.email

    user_exist = await services.user_exist(session , user.email)
    if user_exist:
        raise UserAlreadyExists()


    new_user = await services.create_user(session , user)
    return {"message": "User created successfully" , "user_id": new_user}

@auth_router.post("/login")
async def login(    user: UserLoginModel , session: AsyncSession = Depends(get_session)):
    
    user_email =   user.email
    user_password = user.password

    user = await services.get_user_by_email(session , user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user is not None:
        verify_pass = verify_password(user_password , user.password_hash) 
        if verify_pass:
            access_token = create_access_token(user_data={
                "email": user.email,
                "id": str(user.id),
                "role": user.role
            })
           
            refresh_token = create_access_token(
                user_data={"email": user.email, "id": str(user.id)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )
        return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "id": str(user.id)},
                }
            )
    raise InvalidCredentials()


@auth_router.post("/refresh")
async def get_new_token(token_data: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_data["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_data["user"])

        return JSONResponse(content={"access_token": new_access_token})
    
    raise InvalidToken()

@auth_router.get("/me")
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user

@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK
    )
 