import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from datetime import date

from app.dependencies import get_db_session
from app.models.tenant import Tenant, BackgroundCheckStatus
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


@router.get('/', response_model=APIResponse[list[TenantRead]])
def list_tenants(
    background_check_status: BackgroundCheckStatus | None = Query(default=None),
    tenant_since: date | None = Query(default=None),
    search: str | None = Query(default=None),
    skip: int = Query(default=0),
    limit: int = Query(default=50),
    db: Session = Depends(get_db_session)
):
    query = db.query(Tenant).join(User, Tenant.user_id == User.id)

    if background_check_status:
        query = query.filter(Tenant.background_check_status == background_check_status)
    if tenant_since:
        query = query.filter(Tenant.tenant_since == tenant_since)
    if search:
        term = f"%{search.strip().lower()}%"
        query = query.filter(
            User.first_name.ilike(term) |
            User.last_name.ilike(term) |
            User.email.ilike(term)
        )

    tenants = query.offset(skip).limit(limit).all()

    return {
        'success': True,
        'message': 'Tenants retrieved successfully',
        'data': [TenantRead.model_validate(t) for t in tenants]
    }