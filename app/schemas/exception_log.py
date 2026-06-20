import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ExceptionLogCreate(BaseModel):
    user_id: uuid.UUID | None = None
    error_type: str
    message: str
    stack_trace: str | None = None
    endpoint: str | None = None
    request_method: str | None = None


class ExceptionLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID | None
    error_type: str
    message: str
    stack_trace: str | None
    endpoint: str | None
    request_method: str | None
    created_at: datetime | None
