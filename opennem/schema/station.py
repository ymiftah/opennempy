from typing import List, Optional

from pydantic import Field, field_serializer
from datetime import datetime

from .core import BaseConfig
from .network import NetworkRecordSchema, FueltechSchema


class FacilityStatusSchema(BaseConfig):
    code: str
    label: Optional[str]


class FacilitySchema(BaseConfig):
    id: int
    network: NetworkRecordSchema
    fueltech: Optional[FueltechSchema] = None
    status: Optional[FacilityStatusSchema] = None
    station_id: Optional[int] = None
    code: Optional[str] = None
    dispatch_type: str
    capacity_registered: Optional[float] = None
    registered: Optional[datetime] = None
    deregistered: Optional[datetime] = None
    network_region: Optional[str] = None
    unit_id: Optional[int] = None
    unit_number: Optional[int] = None
    unit_alias: Optional[str] = None
    unit_capacity: Optional[float] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    approved: Optional[bool] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

    @field_serializer('fueltech')
    def serialize_fueltech(self, fueltech: FueltechSchema, _info):
        if fueltech is None:
             return None
        return fueltech.code

    @field_serializer('network')
    def serialize_network(self, network: NetworkRecordSchema, _info):
        if network is None:
            return None
        return network.code

    @field_serializer('status')
    def serialize_status(self, status: FacilityStatusSchema, _info):
        if status is None:
            return None
        return status.code


class StationSchema(BaseConfig):
    id: int
    code: str
    name: Optional[str] = None
    location_id: int
    facilities: List[FacilitySchema]
    approved: Optional[bool] = Field(default=False)
    description: Optional[str] = None
    wikipedia_link: Optional[str] = None
    wikidata_id: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None

    
    @field_serializer('facilities')
    def serialize_facilities(self, facilities: List[FacilitySchema], _info):
        return [facility.id for facility in facilities]
