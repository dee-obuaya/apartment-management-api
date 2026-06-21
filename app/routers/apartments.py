from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid

from app.db.session import get_db
from app.models.apartment import Apartment, ApartmentAmenity
from app.models.owner import Owner
from app.schemas.apartment import ApartmentCreate, ApartmentUpdate, ApartmentRead, ApartmentAmenityCreate, ApartmentAmenityRead
from app.schemas.base import APIResponse
from app.dependencies import get_db_session

router = APIRouter(prefix='/apartments', tags=['Apartments'])


@router.post('/', response_model=APIResponse[ApartmentRead], status_code=201)
def create_apartment(payload: ApartmentCreate, db: Session = Depends(get_db_session)):
    if payload.owner_id:
        owner = db.query(Owner).filter(Owner.id == payload.owner_id).first()
        if not owner:
            raise HTTPException(status_code=404, detail='Owner not found')

    apartment = Apartment(**payload.model_dump())
    db.add(apartment)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail='An apartment wih this unit number already exists')

    db.refresh(apartment)

    return {
        'success': True,
        'message': 'Apartment created successfully',
        'data': ApartmentRead.model_validate(apartment)
    }