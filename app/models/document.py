import uuid
import enum

from sqlalchemy import (
    Column, String, Text, BigInteger, Enum, DateTime, ForeignKey, func, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base


class DocumentType(str, enum.Enum):
    lease_agreement = "lease_agreement"
    lease_addendum = "lease_addendum"
    renewal_letter = "renewal_letter"
    id_document = "id_document"
    background_check = "background_check"
    employment_letter = "employment_letter"
    maintenance_quote = "maintenance_quote"
    maintenance_invoice = "maintenance_invoice"
    maintenance_photo = "maintenance_photo"
    floor_plan = "floor_plan"
    inspection_certificate = "inspection_certificate"
    title_document = "title_document"
    other = "other"


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = (
        CheckConstraint(
            """
            (
                (lease_id IS NOT NULL)::int +
                (tenant_id IS NOT NULL)::int +
                (maintenance_request_id IS NOT NULL)::int +
                (apartment_id IS NOT NULL)::int
            ) = 1
            """,
            name="chk_document_belongs_to_exactly_one_entity"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    lease_id = Column(
        UUID(as_uuid=True),
        ForeignKey("leases.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    maintenance_request_id = Column(
        UUID(as_uuid=True),
        ForeignKey("maintenance_requests.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    apartment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("apartments.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    document_type = Column(
        Enum(DocumentType, name="document_type"),
        nullable=False,
    )
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(1000), nullable=False)
    file_size_bytes = Column(BigInteger, nullable=True)
    mime_type = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)

    uploaded_by_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    lease = relationship("Lease", back_populates="documents")
    tenant = relationship("Tenant", back_populates="documents")
    maintenance_request = relationship("MaintenanceRequest", back_populates="documents")
    apartment = relationship("Apartment", back_populates="documents")
    uploaded_by = relationship("User", back_populates="uploaded_documents")