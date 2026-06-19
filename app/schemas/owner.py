import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, model_validator

from app.schemas.base import UserSummary


class OwnerCreate(BaseModel):
    user_id: uuid.UUID | None = None
    company_name: str | None = None
    contact_email: EmailStr
    contact_phone: str | None = None

    @model_validator(mode='after')
    def check_identity(self) -> 'OwnerCreate':
        if self.user_id is None and self.company_name is None:
            raise ValueError('Either user_id or company_name must be provided')
        return self


class OwnerUpdate(BaseModel):
    company_name: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None


class OwnerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID | None
    company_name: str | None
    contact_email: str
    contact_phone: str | None
    user: UserSummary | None
    created_at: datetime | None
    updated_at: datetime | None
