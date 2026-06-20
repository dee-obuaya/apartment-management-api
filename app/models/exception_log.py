import uuid

from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base


class ExceptionLog(Base):
    __tablename__ = 'exception_logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
    )

    error_type = Column(String(200), nullable=False, index=True)
    message = Column(Text, nullable=False)
    stack_trace = Column(Text, nullable=True)
    endpoint = Column(String(500), nullable=True)
    request_method = Column(String(10), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship('User', back_populates='exception_logs')
