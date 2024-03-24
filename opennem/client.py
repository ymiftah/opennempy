"""OpenNEM API Client Library.

Define the primary API client class for accessing API and data methods of OpenNEM.
"""
import logging
from typing import Dict, List, Optional, Union
from urllib.parse import ParseResult, urlparse

from opennem.core.endpoint import EndpointType, get_opennem_endpoint
from opennem.core.environment import get_environment
from opennem.schema.dataset import OpennemDataSet
from opennem.schema.network import (
    NetworkSchema, NetworkRegionSchema, FueltechSchema, LocationSchema
)
from opennem.schema.station import StationSchema, FacilitySchema
from opennem.settings import settings
from opennem.utils.http import http

logger = logging.getLogger("opennem.api")


class OpenNEMStats(object):
    """OpenNEM Stats Client."""

    def __init__(self, opennem_client):
        pass


class OpenNEMClient(object):
    """
    OpenNEM Core API Client.

    Access API endpoints with an instance of the API client

    .. code:: python
        >>> client = OpenNEMClient()
        >>> networks = client.networks()
        ...
    """

    _base_url: str

    _base_url_parsed: ParseResult

    def __init__(self, base_url: str = None):
        """
        Initialize API client with optional paramters.

        :param base_url: The base API endpoint to access, defaults to None
        :type base_url: str, optional
        """
        env = get_environment(settings.env)

        if base_url:
            self._base_url = base_url
        else:
            self._base_url = get_opennem_endpoint(EndpointType.api, env)

        self._base_url_parsed = urlparse(self._base_url)

    def _get_endpoint(self, endpoint: str) -> str:
        """
        Get the endpoint URI for an endpoint.

        :param endpoint: Path portion of API endpoint
        :type endpoint: str
        :return: Complete API URI
        :rtype: str
        """
        return self._base_url_parsed._replace(path=endpoint).geturl()

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Union[Dict, List]:
        """
        Perform an GET request to an endpoint optionally with parameters for querystring.

        :param endpoint: Endpoint path
        :type endpoint: str
        :param params: Query string parameters, defaults to None
        :type params: Optional[Dict], optional
        :raises Exception: [description]
        :return: JSON response
        :rtype: Union[Dict, List]
        """
        url = self._get_endpoint(endpoint)
        resp = http.get(url, params=params)

        logger.debug("GET [%d] %s", resp.status_code, resp.url)

        if not resp.ok:
            raise Exception("Error from API: {}".format(resp.status_code))

        return resp.json()

    def networks(self) -> List[NetworkSchema]:
        """Return networks."""
        resp = self._get("networks")

        resp_objects = [NetworkSchema(**i) for i in resp]

        return resp_objects

    def network_regions(self, network_id: str) -> List[NetworkRegionSchema]:
        """Return network regions."""
        resp = self._get("networks/regions", {"network_code": network_id})

        resp_objects = [NetworkRegionSchema(**i) for i in resp]

        return resp_objects

    def fueltechs(self) -> List[FueltechSchema]:
        """Return fueltechs."""
        resp = self._get("fueltechs")

        resp_objects = [FueltechSchema(**i) for i in resp]

        return resp_objects

    def facilities(self) -> List[FacilitySchema]:
        """Return fueltechs."""
        resp = self._get("facility")

        resp_objects = [FacilitySchema(**i) for i in resp]

        return resp_objects
    
    def facility(self, facility_code: str) -> FacilitySchema:
        """Return facility."""
        resp = self._get(f"facility/{facility_code}")

        resp_object = FacilitySchema(**resp)

        return resp_object
    
    def locations(self):
        """Return locations."""
        resp = self._get(f"locations")
        # "facility/TESLA_GERALDTON_G1"
        resp_object = [LocationSchema(**i) for i in resp]
        return resp_object
    
    def location(self, id: int):
        """Return location."""
        resp = self._get(f"location/{id}")
        resp_object = LocationSchema(**resp)
        return resp_object
    
    def stations(self):
        """Return station."""
        resp = self._get(f"station")
        resp_object = [StationSchema(**i) for i in resp["data"]]
        return resp_object
    
    def station(self, network_id: int, station_code: str, only_generators=True):
        """Return station."""
        resp = self._get(f"station/{network_id}/{station_code}", params={"only_generators": only_generators})
        resp_object = StationSchema(**resp)
        return resp_object

    def power_network_fueltech(self, network_id: str, network_region_code: str) -> OpennemDataSet:
        """
        Get last 7 days of power generation per fueltech.

        :param network_id: The network code
        :type network_id: str
        :param network_region_code: The network region code
        :type network_id: str
        :raises Exception: Base response
        :return: The data set in OpenNEM Data Set format.
        :rtype: OpennemDataSet
        """
        resp = self._get(f"/stats/power/network/fueltech/{network_id}/{network_region_code}")

        if not isinstance(resp, Dict):
            raise Exception("Bad response type")

        resp_object = OpennemDataSet(**resp)

        return resp_object

    def emission_factors(self, network_id: str) -> OpennemDataSet:
        """
        Get last 7 days of 30 minute emission factors for a network.

        :param network_id: The network code
        :type network_id: str
        :raises Exception: Base response
        :return: The data set in OpenNEM Data Set format.
        :rtype: OpennemDataSet
        """
        resp = self._get(f"/stats/emissionfactor/network/{network_id.strip().upper()}")

        if not isinstance(resp, Dict):
            raise Exception("Bad response type")

        resp_object = OpennemDataSet(**resp)

        return resp_object

    def price(self, network_id: str) -> OpennemDataSet:
        """
        Get price for a network.

        :param network_id: The network code
        :type network_id: str
        :raises Exception: Base response
        :return: The data set in OpenNEM Data Set format.
        :rtype: OpennemDataSet
        """
        resp = self._get(f"/stats/price/{network_id.strip().upper()}")

        if not isinstance(resp, Dict):
            raise Exception("Bad response type")

        resp_object = OpennemDataSet(**resp)

        return resp_object

def main():
    client = OpenNEMClient()
    networks = client.stations()
    return networks

if __name__ == "__main__":
    main()