import uuid
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.user import IdType, UserRole


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone: str | None = None
    id_type: IdType
    id_number: str
    role: UserRole = UserRole.tenant


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    role: UserRole | None = None
    active: bool | None = None


class UserVerifyId(BaseModel):
    id_verified: bool


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    first_name: str
    last_name: str
    date_of_birth: date
    email: str
    phone: str | None
    id_type: IdType
    id_verified: bool
    id_verified_at: datetime | None
    role: UserRole
    active: bool
    created_at: datetime | None
    updated_at: datetime | None
