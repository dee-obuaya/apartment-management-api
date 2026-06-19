import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models.tenant import BackgroundCheckStatus
from app.schemas.base import UserSummary


class TenantCreate(BaseModel):
    user_id: uuid.UUID
    tenant_since: date
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    background_check_status: BackgroundCheckStatus | None = None


class TenantUpdate(BaseModel):
    tenant_since: date | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    background_check_status: BackgroundCheckStatus | None = None


class TenantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user: UserSummary
    tenant_since: date
    emergency_contact_name: str | None
    emergency_contact_phone: str | None
    background_check_status: BackgroundCheckStatus | None
    created_at: datetime | None
    updated_at: datetime | None
