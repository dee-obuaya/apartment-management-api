import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.maintenance import MaintenancePriority
from app.schemas.base import ApartmentSummary, TenantSummary, MaintenanceRequestStatusSummary


class MaintenanceRequestStatusCreate(BaseModel):
    name: str


class MaintenanceRequestStatusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str


class MaintenanceRequestCreate(BaseModel):
    apartment_id: uuid.UUID
    tenant_id: uuid.UUID | None = None
    lease_id: uuid.UUID | None = None
    status_id: uuid.UUID
    title: str
    description: str | None = None
    priority: MaintenancePriority = MaintenancePriority.medium
    estimated_cost: Decimal | None = None
    actual_cost: Decimal | None = None

    @model_validator(mode='after')
    def check_costs(self) -> 'MaintenanceRequestCreate':
        if self.estimated_cost is not None and self.estimated_cost < Decimal('0'):
            raise ValueError('estimated_cost cannot be negative')
        if self.actual_cost is not None and self.actual_cost < Decimal('0'):
            raise ValueError('actual_cost cannot be negative')
        return self


class MaintenanceRequestUpdate(BaseModel):
    status_id: uuid.UUID | None = None
    title: str | None = None
    description: str | None = None
    priority: MaintenancePriority | None = None
    estimated_cost: Decimal | None = None
    actual_cost: Decimal | None = None
    resolved_at: datetime | None = None
    resolution_notes: str | None = None

    @model_validator(mode='after')
    def check_costs(self) -> 'MaintenanceRequestUpdate':
        if self.estimated_cost is not None and self.estimated_cost < Decimal('0'):
            raise ValueError('estimated_cost cannot be negative')
        if self.actual_cost is not None and self.actual_cost < Decimal('0'):
            raise ValueError('actual_cost cannot be negative')
        return self


class MaintenanceRequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    apartment: ApartmentSummary
    tenant: TenantSummary | None
    lease_id: uuid.UUID | None
    status: MaintenanceRequestStatusSummary
    title: str
    description: str | None
    priority: MaintenancePriority
    estimated_cost: Decimal | None
