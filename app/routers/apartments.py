from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
from decimal import Decimal

from app.db.session import get_db
from app.models.apartment import Apartment, ApartmentAmenity, ApartmentStatus
from app.models.owner import Owner
from app.schemas.apartment import ApartmentCreate, ApartmentUpdate, ApartmentRead, ApartmentAmenityCreate, ApartmentAmenityRead
from app.schemas.base import APIResponse
from app.dependencies import get_db_session


router = APIRouter(prefix='/apartments', tags=['Apartments'])


@router.get('/', response_model=APIResponse[list[ApartmentRead]])
def list_apartments(
    status: ApartmentStatus | None = Query(default=None),
    owner_id: uuid.UUID | None = Query(default=None),
    bedrooms: int | None = Query(default=None),
    min_price: Decimal | None = Query(default=None),
    max_price: Decimal | None = Query(default=None),
    skip: int = Query(default=0),
    limit: int = Query(default=50),
    db: Session = Depends(get_db_session)
):
    query = db.query(Apartment)

    if status:
        query = query.filter(Apartment.status == status)
    if owner_id:
        query = query.filter(Apartment.owner_id == owner_id)
    if bedrooms is not None:
        query = query.filter(Apartment.bedrooms == bedrooms)
    if min_price is not None:
        query = query.filter(Apartment.price >= min_price)
    if max_price is not None:
        query = query.filter(Apartment.price <= max_price)

    apartments = query.offset(skip).limit(limit).all()

    return {
        'success': True,
        'message': 'Apartments retrieved successfully',
        'data': [ApartmentRead.model_validate(a) for a in apartments]
    }
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