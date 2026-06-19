import uuid
import enum

from sqlalchemy import (
    Column, String, Text, Numeric, Enum, DateTime, ForeignKey, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base


class MaintenancePriority(str, enum.Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'
    emergency = 'emergency'


class MaintenanceRequestStatus(Base):
    __tablename__ = 'maintenance_request_statuses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True)

    requests = relationship('MaintenanceRequest', back_populates='status')

    def __repr__(self):
        return f'<MaintenanceRequestStatus name={self.name!r}>'


class MaintenanceRequest(Base):
    __tablename__ = 'maintenance_requests'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    apartment_id = Column(
        UUID(as_uuid=True),
        ForeignKey('apartments.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
    )
    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey('tenants.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )
    lease_id = Column(
        UUID(as_uuid=True),
        ForeignKey('leases.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )
    status_id = Column(
        UUID(as_uuid=True),
        ForeignKey('maintenance_request_statuses.id', ondelete='RESTRICT'),
        nullable=False,
    )

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(
        Enum(MaintenancePriority, name='maintenance_priority'),
        nullable=False,
        default=MaintenancePriority.medium,
    )

    estimated_cost = Column(Numeric(12, 2), nullable=True)
    actual_cost = Column(Numeric(12, 2), nullable=True)

    reported_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    resolution_notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    apartment = relationship('Apartment', back_populates='maintenance_requests')
    tenant = relationship('Tenant', back_populates='maintenance_requests')
    lease = relationship('Lease', back_populates='maintenance_requests')
    status = relationship('MaintenanceRequestStatus', back_populates='requests')
    documents = relationship('Document', back_populates='maintenance_request')

    def __repr__(self):
        return f'<MaintenanceRequest id={self.id} title={self.title!r} priority={self.priority!r}>'