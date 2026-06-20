import uuid
import enum

from sqlalchemy import (
    Column, String, Text, Integer, SmallInteger, Numeric,
    Enum, DateTime, ForeignKey, UniqueConstraint, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base


class ApartmentStatus(str, enum.Enum):
    vacant = 'vacant'
    occupied = 'occupied'
    maintenance = 'maintenance'
    unlisted = 'unlisted'

class Apartment(Base):
    __tablename__ = 'apartments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('owners.id', ondelete='RESTRICT'), nullable=True)
    unit_number = Column(String(20), nullable=False, unique=True)
    description = Column(Text)
    floor = Column(Integer)
    bedrooms = Column(SmallInteger, nullable=False)
    bathrooms = Column(Numeric(3,1), nullable=False)
    square_footage = Column(Numeric(8,2))
    price = Column(Numeric(12,2) , nullable=False)
    service_charge = Column(Numeric(12, 2), nullable=False, default=0)
    deposit_amount = Column(Numeric(12, 2), nullable=False, default=0)
    status = Column(
        Enum(ApartmentStatus, name='apartment_status'),
        nullable=False,
        default=ApartmentStatus.vacant
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner = relationship('Owner', back_populates='apartments')
    amenities = relationship('ApartmentAmenity', back_populates='apartment')
    leases = relationship('Lease', back_populates='apartment')
    maintenance_requests = relationship('MaintenanceRequest', back_populates='apartment')
    documents = relationship('Document', back_populates='apartment')
    applications = relationship('Application', back_populates='apartment')

class ApartmentAmenity(Base):
    __tablename__ = 'apartment_amenities'
    __table_args__ = (
        UniqueConstraint('apartment_id', 'amenity_name', name='uq_apartment_amenity'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apartment_id = Column(UUID(as_uuid=True), ForeignKey('apartments.id', ondelete='CASCADE'), nullable=False)
    amenity_name = Column(String(100), nullable=False)

    apartment = relationship('Apartment', back_populates='amenities')