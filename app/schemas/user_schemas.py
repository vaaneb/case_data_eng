from __future__ import annotations
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    """Schema for creating a user."""
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str


class UserGetSchema(BaseModel):
    """Response schema for reading a user."""
    id: UUID
    first_name: str
    last_name: str
    email: str
    phone: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    """Schema for updating a user - all fields optional for partial updates."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None

    class Config:
        extra = 'forbid'
