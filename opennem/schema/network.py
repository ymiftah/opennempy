from typing import List, Optional, Any

from pydantic import Field
from datetime import datetime

from .core import BaseConfig
from datetime import datetime


class NetworkRegionSchema(BaseConfig):
    """Defines a network region"""

    code: str
    timezone: Optional[str] = Field(None, description="Network region timezone")


class NetworkSchema(BaseConfig):
    """Defines a network"""

    code: str
    country: str
    label: str

    regions: Optional[List[NetworkRegionSchema]]
    timezone: Optional[str] = Field(None, description="Network timezone")
    interval_size: int = Field(..., description="Size of network interval in minutes")


class FueltechSchema(BaseConfig):
    code: str
    label: Optional[str]
    renewable: Optional[bool]


class NetworkRecordSchema(BaseConfig):
    code: str


class RecordSchema(BaseConfig):
    id: Optional[int] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    locality: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[str] = None
    country: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


# class ParticipantSchema(BaseConfig):
#     id: int
#     code: Optional[str] = None
#     name: str
#     network_name: Optional[str] = None
#     network_code: Optional[str] = None
#     country: Optional[str] = None
#     abn: Optional[str] = None

# class PhotoSchema(BaseConfig):
#     hash_id: str
#     width: int
#     height: int
#     photo_url: Optional[str] = None
#     license_type: Optional[str] = None
#     license_link: Optional[str] = None
#     author: Optional[str] = None
#     author_link: Optional[str] = None
#     is_primary: Optional[bool] = None
#     order: Optional[int] = None


class GeomSchema(BaseConfig):
    property1: Optional[str] = None
    property2: Optional[str] = None


class LocationSchema(BaseConfig):
    version: Optional[str] = None
    created_at: Optional[datetime] = None
    response_status: Optional[str] = None
    total_records: Optional[int] = None
    record: Optional[RecordSchema] = None

    id: Optional[int] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    locality: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[str] = None
    country: Optional[str] = Field(default="au")
    geocode_approved: Optional[bool] = Field(default=False)
    geocode_processed_at: Optional[datetime] = None
    geocode_by: Optional[str] = None
    geom: Optional[GeomSchema] = None
    boundary: Optional[Any] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
