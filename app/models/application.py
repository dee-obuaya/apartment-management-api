import uuid
import enum

from sqlalchemy import (
    Column, String, Date, Text, Enum, DateTime, ForeignKey, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base


class ApplicationStatus(str, enum.Enum):
    submitted = 'submitted'
    under_review = 'under_review'
    approved = 'approved'
    rejected = 'rejected'


class Application(Base):
    __tablename__ = 'applications'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    apartment_id = Column(
        UUID(as_uuid=True),
        ForeignKey('apartments.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
    )
    reviewed_by_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )

    # personal details
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    emergency_contact_name = Column(String(200), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)

    # application tracking
    status = Column(
        Enum(ApplicationStatus, name='application_status'),
        nullable=False,
        default=ApplicationStatus.submitted,
    )
    notes = Column(Text, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    apartment = relationship('Apartment', back_populates='applications')
    reviewed_by = relationship('User', back_populates='reviewed_applications')