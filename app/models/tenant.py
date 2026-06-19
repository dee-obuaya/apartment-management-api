import uuid
import enum

from sqlalchemy import Column, String, Date, DateTime, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base

class BackgroundCheckStatus(str, enum.Enum):
    pending = "pending"
    passed = "passed"
    failed = "failed"
    waived = "waived"

class Tenant(Base):
    __tablename__ = 'tenants'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='RESTRICT'), nullable=False, unique=True)
    tenant_since = Column(Date, nullable=False)
    emergency_contact_name = Column(String(200))
    emergency_contact_phone = Column(String(20))
    background_check_status = Column(
        Enum(BackgroundCheckStatus, name='background_check_status'),
        nullable=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='tenant_profile')
    leases = relationship('Lease', back_populates='tenant')
    maintenance_requests = relationship('MaintenanceRequest', back_populates='tenant')
    documents = relationship('Document', back_populates='tenant')