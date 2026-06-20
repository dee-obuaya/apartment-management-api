import uuid

from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict

from app.models.user import IdType, UserRole
from app.models.tenant import BackgroundCheckStatus
from app.models.apartment import ApartmentStatus

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: T | None = None


class UserSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    first_name: str
    last_name: str
    email: str
    role: UserRole


class TenantSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user: UserSummary
    background_check_status: BackgroundCheckStatus | None


class OwnerSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_name: str | None
    contact_email: str
    contact_phone: str | None


class ApartmentSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    unit_number: str
    floor: int | None
    bedrooms: int
    status: ApartmentStatus


class MaintenanceRequestStatusSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str