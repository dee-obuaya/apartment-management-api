import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from decimal import Decimal

from app.dependencies import get_db_session
from app.models.apartment import Apartment, ApartmentAmenity, ApartmentStatus
from app.models.owner import Owner
from app.schemas.apartment import ApartmentCreate, ApartmentUpdate, ApartmentRead, ApartmentAmenityPayload, ApartmentAmenityRead
from app.schemas.base import APIResponse


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


@router.get('/{apartment_id}', response_model=APIResponse[ApartmentRead])
def get_apartment(apartment_id: uuid.UUID, db: Session = Depends(get_db_session)):
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail='Apartment not found')

    return {
        'success': True,
        'message': 'Apartment retrieved successfully',
        'data': ApartmentRead.model_validate(apartment)
    }


@router.patch('/{apartment_id}', response_model=APIResponse[ApartmentRead])
def update_apartment(
    apartment_id: uuid.UUID,
    payload: ApartmentUpdate,
    db: Session = Depends(get_db_session)
):
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail='Apartment not found')

    if payload.owner_id:
        owner = db.query(Owner).filter(Owner.id == payload.owner_id).first()
        if not owner:
            raise HTTPException(status_code=404, detail='Owner not found')

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(apartment, field, value)

    db.commit()
    db.refresh(apartment)

    return {
        'success': True,
        'message': 'Apartment updated successfully',
        'data': ApartmentRead.model_validate(apartment)
    }


@router.post('/{apartment_id}/amenities', response_model=APIResponse[ApartmentRead], status_code=201)
def add_amenities(
    apartment_id: uuid.UUID,
    payload: ApartmentAmenityPayload,
    db: Session = Depends(get_db_session)
):
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail='Apartment not found')

    existing = {a.amenity_name for a in apartment.amenities}
    unique_new = list(dict.fromkeys(a.strip() for a in payload.amenities))

    for name in unique_new:
        if name not in existing:
            db.add(ApartmentAmenity(apartment_id=apartment_id, amenity_name=name))

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail='One or more amenities already exist for this apartment')

    return {
        'success': True,
        'message': 'Amenities added successfully',
        'data': ApartmentRead.model_validate(apartment)
    }


@router.delete('/{apartment_id}/amenities/{amenity_id}', status_code=204)
def delete_amenity(
    apartment_id: uuid.UUID,
    amenity_id: uuid.UUID,
    db: Session = Depends(get_db_session)
):
    amenity = db.query(ApartmentAmenity).filter(
        ApartmentAmenity.id == amenity_id,
        ApartmentAmenity.apartment_id == apartment_id
    ).first()

    if not amenity:
        raise HTTPException(status_code=404, detail='Amenity not found')

    db.delete(amenity)
    db.commit()


@router.put('/{apartment_id}/amenities', response_model=APIResponse[ApartmentRead])
def replace_amenities(
    apartment_id: uuid.UUID,
    payload: ApartmentAmenityPayload,
    db: Session = Depends(get_db_session)
):
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, details='Apartment not found')

    db.query(ApartmentAmenity).filter(ApartmentAmenity.apartment_id == apartment_id).delete()

    unique_amenities = list(dict.fromkeys(a.strip() for a in payload.amenities))
    for name in unique_amenities:
        db.add(ApartmentAmenity(apartment_id=apartment_id, amenity_name=name))

    db.commit()

    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()

    return{
        'success': True,
        'message': 'Amenities updated successfully',
        'data': ApartmentRead.model_validate(apartment)
    }


@router.delete('/{apartment_id}', status_code=204)
def delete_apartment(apartment_id: uuid.UUID, db: Session = Depends(get_db_session)):
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail='Apartment not found')

    try:
        db.delete(apartment)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # print(f"IntegrityError: {e.orig}")
        raise HTTPException(
            status_code=400,
            detail='Apartment cannot be deleted while it has active leases or other assignments'
        )