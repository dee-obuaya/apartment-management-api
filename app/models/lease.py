import uuid
import enum

from sqlalchemy import (
    Column, Date, Numeric, Enum, DateTime, ForeignKey, CheckConstraint, Text, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base


class LeaseStatus(str, enum.Enum):
    pending = 'pending'
    active = 'active'
    ended = 'ended'
    terminated = 'terminated'


class LeaseTerminationReason(str, enum.Enum):
    non_payment = "non_payment"
    lease_violation = "lease_violation"
    tenant_request = "tenant_request"
    owner_request = "owner_request"
    property_damage = "property_damage"
    other = "other"


class Lease(Base):
    __tablename__ = 'leases'
    __table_args__ = (
        CheckConstraint('lease_end > lease_start', name='chk_lease_dates'),
        CheckConstraint(
            'move_out_date IS NULL OR move_in_date IS NULL OR move_out_date >= move_in_date',
            name='chk_move_out_after_in'
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='RESTRICT'), nullable=False)
    apartment_id = Column(UUID(as_uuid=True), ForeignKey('apartments.id', ondelete='RESTRICT'), nullable=False)
    lease_start = Column(Date, nullable=False)
    lease_end = Column(Date, nullable=False)
    move_in_date = Column(Date)
    move_out_date = Column(Date)
    rent_amount = Column(Numeric(12, 2), nullable=False)
    service_charge = Column(Numeric(12, 2), nullable=False, default=0)
    deposit_amount = Column(Numeric(12, 2), nullable=False, default=0)
    status = Column(Enum(LeaseStatus, name='lease_status'), nullable=False, default=LeaseStatus.pending)
    termination_reason = Column(Enum(LeaseTerminationReason, name="lease_termination_reason"), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    tenant = relationship('Tenant', back_populates='leases')
    apartment = relationship('Apartment', back_populates='leases')
    payments = relationship('Payment', back_populates='lease')