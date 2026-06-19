import uuid
import enum

from sqlalchemy import Column, Date, Numeric, Enum, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base


class PaymentType(str, enum.Enum):
    rent = 'rent'
    service_charge = 'service_charge'
    deposit = 'deposit'


class PaymentStatus(str, enum.Enum):
    pending = 'pending'
    paid = 'paid'
    overdue = 'overdue'
    partial = 'partial'
    cancelled = 'cancelled'


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lease_id = Column(UUID(as_uuid=True), ForeignKey('leases.id', ondelete='RESTRICT'), nullable=False)
    payment_type = Column(Enum(PaymentType, name='payment_type'), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    amount_paid = Column(Numeric(12, 2), nullable=False, default=0)
    due_date = Column(Date, nullable=False)
    paid_date = Column(Date)
    status = Column(
        Enum(PaymentStatus, name='payment_status'),
        nullable=False, default=PaymentStatus.pending
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    lease = relationship('Lease', back_populates='payments')
