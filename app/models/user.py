import uuid
import enum

from sqlalchemy import (
    Column, String, Date, Boolean, DateTime, Enum, LargeBinary, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base

class IdType(str, enum.Enum):
    passport = 'passport'
    national_id = 'national_id'
    drivers_license = 'drivers_license'

class UserRole(str, enum.Enum):
    tenant = 'tenant'
    owner = 'owner'
    staff = 'staff'
    admin = 'admin'

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20))
    id_type = Column(Enum(IdType, name='id_type'), nullable=False)
    id_number_encrypted = Column(LargeBinary, nullable=False)
    id_number_hash = Column(String(64), nullable=False, unique=True)
    id_verified = Column(Boolean, nullable=False, default=False)
    id_verified_at = Column(DateTime(timezone=True))
    role = Column(Enum(UserRole, name='user_role'), nullable=False, default=UserRole.tenant)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    tenant_profile = relationship('Tenant', back_populates='user', uselist=False)
    owner_profile = relationship('Owner', back_populates='user', uselist=False)
    uploaded_documents = relationship('Document', back_populates='uploaded_by')
    action_logs = relationship('ActionLog', back_populates='user')
    exception_logs = relationship('ExceptionLog', back_populates='user')
    reviewed_applications = relationship('Application', back_populates='user')
    created_templates = relationship('Template', back_populates='created_by')