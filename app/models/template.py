import uuid

from sqlalchemy import (
    Column, String, Text, Boolean, Enum, DateTime, ForeignKey, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.models.document import DocumentType


class Template(Base):
    __tablename__ = 'templates'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    created_by_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )

    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    document_type = Column(
        Enum(DocumentType, name='document_type'),
        nullable=False,
    )
    file_path = Column(String(1000), nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    created_by = relationship('User', back_populates='created_templates')