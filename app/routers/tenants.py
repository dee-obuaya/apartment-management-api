import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.dependencies import get_db_session
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantRead
from app.schemas.base import APIResponse


router = APIRouter(prefix='/tenants', tags=['Tenants'])


@router.post('/', response_model=APIResponse[TenantRead], status_code=201)
def create_tenant(payload: TenantCreate, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    existing = db.query(Tenant).filter(Tenant.user_id == payload.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail='A tenant profile already exists for this user')


    tenant = Tenant(**payload.model_dump())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return {
        'success': True,
        'message': 'Tenant created successfully',
        'data': TenantRead.model_validate(tenant)
    }