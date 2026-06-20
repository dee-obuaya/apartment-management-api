import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.dependencies import get_db_session
from app.models.owner import Owner
from app.schemas.owner import OwnerCreate, OwnerUpdate, OwnerRead
from app.schemas.base import APIResponse

router = APIRouter(prefix='/owners', tags=['Owners'])

@router.get('/', response_model=APIResponse[list[OwnerRead]])
def list_owners(
    skip: int = 0,
    limit: int = 0,
    db: Session = Depends(get_db_session)
):
    owners = db.query(Owner).offset(skip).limit(limit).all()

    return {
        'success': True,
        'message': 'Owners retrieved successfully',
        'data': [OwnerRead.model_validate(o) for o in owners]
    }

@router.get('/{owner_id}', response_model=APIResponse[OwnerRead])
def get_owner(owner_id: uuid.UUID, db: Session = Depends(get_db_session)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail='Owner not found')
    
    return {
        'success': True,
        'message': 'Owner retrieved successfully',
        'data': OwnerRead.model_validate(owner)
    }

@router.post('/', response_model=APIResponse[OwnerRead], status_code=201)
def create_owner(payload: OwnerCreate, db: Session = Depends(get_db_session)):
    if payload.user_id:
        from app.models.user import User
        user = db.query(User).filter(User.id ==payload.user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        
        existing = db.query(Owner).filter(Owner.user_id == payload.user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail='User already has an owner profile')
        
    owner = Owner(
        user_id=payload.user_id,
        company_name=payload.company_name,
        contact_email=payload.contact_email,
        contact_phone=payload.contact_phone,
    )
    db.add(owner)
    db.commit()
    db.refresh(owner)

    return {
        'success': True,
        'message': 'Owner created successfully',
        'data': OwnerRead.model_validate(owner)
    }
    

@router.patch('/{owner_id}', response_model=APIResponse[OwnerRead])
def update_owner(
    owner_id: uuid.UUID,
    payload: OwnerUpdate,
    db: Session = Depends(get_db_session)
):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail='Owner not found')

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(owner, field, value)

    db.commit()
    db.refresh(owner)

    return {
        'success': True,
        'message': 'Owner updated successfully',
        'data': OwnerRead.model_validate(owner)
    }


@router.delete('/{owner_id}', status_code=204)
def delete_owner(owner_id: uuid.UUID, db: Session = Depends(get_db_session)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail='Owner not found')

    try:
        db.delete(owner)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail='Owner cannot be deleted while they have assignments assigned'
        )
