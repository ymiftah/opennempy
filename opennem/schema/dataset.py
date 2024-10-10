"""
OpenNEM Stat Data Schemas.

These schemas define the format data is returned in.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Tuple

from pydantic import field_validator

from opennem.core.offsets import delta_from_human_interval
from opennem.schema.core import BaseConfig
from opennem.schema.interval import TimeInterval
from opennem.schema.period import TimePeriod
from opennem.schema.stat import StatType
from opennem.schema.validators import (
    chop_microseconds,
    data_validate,
    optionally_parse_string_datetime,
)


class OpennemDataHistory(BaseConfig):

    """The start date of the data series.

    :return: [description]
    :rtype: [type]
    """

    start: datetime

    """[summary]

    :return: [description]
    :rtype: [type]
    """
    last: datetime

    interval: str

    data: List

    # validators
    _data_valid = field_validator("data")(data_validate)

    def values(self) -> List[Tuple[datetime, float]]:
        """[summary]

        :return: [description]
        :rtype: List[Tuple[datetime, float]]
        """
        interval_obj = delta_from_human_interval(self.interval)
        inclusive = False
        dt = self.start

        if interval_obj.minutes > 0:
            inclusive = True

        # return as list rather than generate
        timeseries_data = []

        # rewind back one interval
        if inclusive:
            # dt -= interval_obj
            pass

        for v in self.data:
            timeseries_data.append((dt, v))
            dt = dt + interval_obj

        return timeseries_data


class OpennemData(BaseConfig):
    """[summary]

    :param BaseConfig: [description]
    :type BaseConfig: [type]
    """

    id: Optional[str] = None
    type: Optional[str] = None
    code: Optional[str] = None
    network: Optional[str] = None
    data_type: str
    units: str

    fuel_tech: Optional[str] = None

    region: Optional[str] = None

    interval: Optional[TimeInterval] = None
    period: Optional[TimePeriod] = None

    history: OpennemDataHistory
    forecast: Optional[OpennemDataHistory] = None

    x_capacity_at_present: Optional[float] = None


class OpennemDataSet(BaseConfig):
    type: Optional[str] = None
    version: Optional[str] = None
    network: Optional[str] = None
    code: Optional[str] = None
    region: Optional[str] = None
    created_at: Optional[datetime] = None
    feature_flags: Optional[List[str]] = None
    messages: Optional[List[str]] = None

    data: List[OpennemData]

    def get_id(self, id: str) -> Optional[OpennemData]:
        return next(filter(lambda x: x.id == id, self.data), None)

    # validators
    _version_fromstr = field_validator("created_at")(
        optionally_parse_string_datetime
    )

    _created_at_trim = field_validator("created_at")(chop_microseconds)

    def get_by_stat_type(self, stat_type: StatType) -> OpennemDataSet:
        em = self.copy()
        em.data = list(filter(lambda s: s.data_type == stat_type, self.data))
        return em

    def get_by_network_id(
        self,
        network_id: str,
    ) -> OpennemDataSet:
        em = self.copy()
        em.data = list(filter(lambda s: s.network.code == network_id, self.data))
        return em

    def get_by_network_region(
        self,
        network_region: str,
    ) -> OpennemDataSet:
        em = self.copy()
        em.data = list(filter(lambda s: s.region == network_region, self.data))
        return em

    def get_by_year(
        self,
        year: int,
    ) -> OpennemDataSet:
        em = self.copy()
        em.data = list(filter(lambda s: s.year == year, self.data))
        return em

    def get_by_years(
        self,
        years: List[int],
    ) -> OpennemDataSet:
        em = self.copy()
        em.data = list(filter(lambda s: s.year in years, self.data))
        return em
