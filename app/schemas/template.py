import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.document import DocumentType


class TemplateCreate(BaseModel):
    name: str
    description: str | None = None
    document_type: DocumentType
    file_path: str
    active: bool = True
    created_by_user_id: uuid.UUID | None = None


class TemplateUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    document_type: DocumentType | None = None
    file_path: str | None = None
    active: bool | None = None


class TemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    document_type: DocumentType
    file_path: str
    active: bool
    created_by_user_id: uuid.UUID | None
    created_at: datetime | None
    updated_at: datetime | None
