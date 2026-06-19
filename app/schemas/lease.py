import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.lease import LeaseStatus, LeaseTerminationReason
from app.schemas.base import TenantSummary, ApartmentSummary


class LeaseCreate(BaseModel):
    tenant_id: uuid.UUID
    apartment_id: uuid.UUID
    lease_start: date
    lease_end: date
    move_in_date: date | None = None
    move_out_date: date | None = None
    rent_amount: Decimal
    service_charge: Decimal = Decimal('0')
    deposit_amount: Decimal = Decimal('0')
    status: LeaseStatus = LeaseStatus.pending
    notes: str | None = None

    @model_validator(mode='after')
    def check_dates(self) -> 'LeaseCreate':
        if self.lease_end <= self.lease_start:
            raise ValueError('lease_end must be after lease_start')
        if (
            self.move_out_date is not None
            and self.move_in_date is not None
            and self.move_out_date < self.move_in_date
        ):
            raise ValueError('move_out_date must be on or after move_in_date')
        return self


class LeaseUpdate(BaseModel):
    lease_end: date | None = None
    move_in_date: date | None = None
    move_out_date: date | None = None
    rent_amount: Decimal | None = None
    service_charge: Decimal | None = None
    deposit_amount: Decimal | None = None
    status: LeaseStatus | None = None
    notes: str | None = None


class LeaseTerminate(BaseModel):
    termination_reason: LeaseTerminationReason
    notes: str | None = None


class LeaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant: TenantSummary
    apartment: ApartmentSummary
    lease_start: date
    lease_end: date
    move_in_date: date | None
    move_out_date: date | None
    rent_amount: Decimal
    service_charge: Decimal
    deposit_amount: Decimal
    status: LeaseStatus
    termination_reason: LeaseTerminationReason | None
    notes: str | None
    created_at: datetime | None
    updated_at: datetime | None
