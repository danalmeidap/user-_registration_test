from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    username: str
    email: EmailStr


class UserDB(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
