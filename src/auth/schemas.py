from pydantic import BaseModel , Field
import uuid  
from datetime import datetime

class UserCreate(BaseModel):
    name : str
    username : str
    email : str
    password : str

class UserModel(BaseModel):
    
    id: uuid.UUID
    username: str
    email: str
    name: str
    is_verified: bool
    created_at: datetime
    update_at: datetime

class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)