from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from sqlmodel import select
from src.auth.schemas import UserCreate 
from src.db.models import User
from .utils import generate_passwd_hash , verify_password

class UserService:
    async def get_user_by_email(self , session : AsyncSession ,  email : str):
        query = select(User).where(User.email ==  email)
        result  = await session.execute(query)
        user = result.scalars().first()
        return user 
    
    async def user_exist(self , session : AsyncSession , email : str):
        user = await self.get_user_by_email(session , email)
        return user is not None 
    
    async def create_user(self , session : AsyncSession , user : UserCreate):
        user_data_dict = user.model_dump()
        new_user = User(**user_data_dict)

        new_user.password_hash = generate_passwd_hash(user_data_dict["password"])
        new_user.role = "user"
        

        session.add(new_user)
        await session.commit()
        return new_user  
    
