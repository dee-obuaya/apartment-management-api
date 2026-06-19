import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.payment import PaymentType, PaymentStatus


class PaymentCreate(BaseModel):
    lease_id: uuid.UUID
    payment_type: PaymentType
    amount: Decimal
    amount_paid: Decimal = Decimal('0')
    due_date: date
    paid_date: date | None = None
    status: PaymentStatus = PaymentStatus.pending

    @model_validator(mode='after')
    def check_amount_paid(self) -> 'PaymentCreate':
        if self.amount_paid < Decimal('0'):
            raise ValueError('amount_paid cannot be negative')
        if self.amount_paid > self.amount:
            raise ValueError('amount_paid cannot exceed amount')
        if self.amount <= Decimal('0'):
            raise ValueError('amount must be greater than zero')
        return self


class PaymentUpdate(BaseModel):
    amount_paid: Decimal | None = None
    paid_date: date | None = None
    status: PaymentStatus | None = None

    @model_validator(mode='after')
    def check_amount_paid(self) -> 'PaymentUpdate':
        if self.amount_paid is not None and self.amount_paid < Decimal('0'):
            raise ValueError('amount_paid cannot be negative')
        return self


class PaymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lease_id: uuid.UUID
    payment_type: PaymentType
    amount: Decimal
    amount_paid: Decimal
    due_date: date
    paid_date: date | None
    status: PaymentStatus
    created_at: datetime | None
    updated_at: datetime | None
