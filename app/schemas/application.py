import uuid
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.application import ApplicationStatus
from app.schemas.base import ApartmentSummary


class ApplicationCreate(BaseModel):
    apartment_id: uuid.UUID
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None


class ApplicationUpdate(BaseModel):
    status: ApplicationStatus | None = None
    notes: str | None = None
    reviewed_by_user_id: uuid.UUID | None = None
    reviewed_at: datetime | None = None


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    apartment: ApartmentSummary
    first_name: str
    last_name: str
    date_of_birth: date
    email: str
    phone: str | None
    emergency_contact_name: str | None
    emergency_contact_phone: str | None
    status: ApplicationStatus
    notes: str | None
    reviewed_by_user_id: uuid.UUID | None
    reviewed_at: datetime | None
    created_at: datetime | None
    updated_at: datetime | None
