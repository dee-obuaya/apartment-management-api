import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base

class Owner (Base):
    __tablename__ = 'owners'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    company_name = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            'user_id IS NOT NULL OR company_name IS NOT NULL',
            name='chk_owner_has_identity'
        ),
    )

    user = relationship('User', back_populates='owner_profile')
    apartments = relationship('Apartment', back_populates='owner')