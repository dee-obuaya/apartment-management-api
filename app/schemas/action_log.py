import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.schemas.base import UserSummary


class ActionLogCreate(BaseModel):
    user_id: uuid.UUID | None = None
    action: str
    entity_type: str
    entity_id: uuid.UUID | None = None
    extra_data: dict[str, Any] | None = None


class ActionLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user: UserSummary | None
    action: str
    entity_type: str
    entity_id: uuid.UUID | None
    extra_data: dict[str, Any] | None
    created_at: datetime | None
