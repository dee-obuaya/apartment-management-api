import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.apartment import ApartmentStatus
from app.schemas.base import OwnerSummary


class ApartmentAmenityPayload(BaseModel):
    amenities: list[str]


class ApartmentAmenityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    amenity_name: str


class ApartmentCreate(BaseModel):
    owner_id: uuid.UUID | None = None
    unit_number: str
    description: str | None = None
    floor: int | None = None
    bedrooms: int
    bathrooms: Decimal
    square_footage: Decimal | None = None
    price: Decimal
    service_charge: Decimal = Decimal('0')
    deposit_amount: Decimal = Decimal('0')
    status: ApartmentStatus = ApartmentStatus.vacant


class ApartmentUpdate(BaseModel):
    owner_id: uuid.UUID | None = None
    description: str | None = None
    floor: int | None = None
    bedrooms: int | None = None
    bathrooms: Decimal | None = None
    square_footage: Decimal | None = None
    price: Decimal | None = None
    service_charge: Decimal | None = None
    deposit_amount: Decimal | None = None
    status: ApartmentStatus | None = None


class ApartmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    unit_number: str
    description: str | None
    floor: int | None
    bedrooms: int
    bathrooms: Decimal
    square_footage: Decimal | None
    price: Decimal
    service_charge: Decimal
    deposit_amount: Decimal
    status: ApartmentStatus
    owner: OwnerSummary | None
    amenities: list[ApartmentAmenityRead]
    created_at: datetime | None
    updated_at: datetime | None
