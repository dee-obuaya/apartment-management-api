import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.document import DocumentType, DocumentStatus


class DocumentCreate(BaseModel):
    lease_id: uuid.UUID | None = None
    tenant_id: uuid.UUID | None = None
    maintenance_request_id: uuid.UUID | None = None
    apartment_id: uuid.UUID | None = None
    document_type: DocumentType
    file_name: str
    file_path: str
    file_size_bytes: int | None = None
    mime_type: str | None = None
    notes: str | None = None
    uploaded_by_user_id: uuid.UUID | None = None

    @model_validator(mode='after')
    def check_exactly_one_entity(self) -> 'DocumentCreate':
        filled = sum([
            self.lease_id is not None,
            self.tenant_id is not None,
            self.maintenance_request_id is not None,
            self.apartment_id is not None,
        ])
        if filled != 1:
            raise ValueError(
                'A document must be linked to exactly one of: '
                'lease_id, tenant_id, maintenance_request_id, apartment_id'
            )
        return self


class DocumentUpdate(BaseModel):
    document_type: DocumentType | None = None
    status: DocumentStatus | None = None
    file_name: str | None = None
    file_path: str | None = None
    file_size_bytes: int | None = None
    mime_type: str | None = None
    notes: str | None = None


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lease_id: uuid.UUID | None
    tenant_id: uuid.UUID | None
    maintenance_request_id: uuid.UUID | None
    apartment_id: uuid.UUID | None
    document_type: DocumentType
    status: DocumentStatus | None
    file_name: str
    file_path: str
    file_size_bytes: int | None
    mime_type: str | None
    notes: str | None
    uploaded_by_user_id: uuid.UUID | None
    created_at: datetime | None
    updated_at: datetime | None
