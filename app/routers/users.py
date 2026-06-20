import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.dependencies import get_db_session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserVerifyId, UserRead
from app.schemas.base import APIResponse

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', response_model=APIResponse[list[UserRead]])
def list_users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db_session)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return {
        'success': True,
        'message': 'Users retrieved successfully',
        'data': [UserRead.model_validate(u) for u in users]
    }

@router.get('/{user_id}', response_model=APIResponse[UserRead])
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    return {
        'success': True,
        'message': 'User retrieved successfully',
        'data': UserRead.model_validate(user)
    }


@router.post('/', response_model=APIResponse[UserRead], status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db_session)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    
    user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        date_of_birth=payload.date_of_birth,
        email=payload.email,
        phone=payload.phone,
        id_type=payload.id_type,
        id_number_encrypted=payload.id_number.encode(),
        id_number_hash=str(hash(payload.id_number)),
        role=payload.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        'success': True,
        'message': 'User created successfully',
        'data': UserRead.model_validate(user)
    }


@router.patch('/{user_id}', response_model=APIResponse[UserRead])
def update_user(
    user_id: uuid.UUID,
    payload: UserUpdate,
    db: Session = Depends(get_db_session)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return {
        'success': True,
        'message': 'User updated successfully',
        'data': UserRead.model_validate(user)
    }


@router.post('/{user_id}/verify-id', response_model=APIResponse[UserRead])
def verify_user_id(
    user_id: uuid.UUID,
    payload: UserVerifyId,
    db: Session = Depends(get_db_session)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    user.id_verified = payload.id_verified
    user.id_verified_at = datetime.now(timezone.utc) if payload.id_verified else None

    db.commit()
    db.refresh(user)

    return {
        'success': True,
        'message': 'User ID verification updated',
        'data': UserRead.model_validate(user)
    }

@router.delete('/{user_id}', status_code=204)
def deactivate_user(user_id: uuid.UUID, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    user.active = False
    db.commit()
