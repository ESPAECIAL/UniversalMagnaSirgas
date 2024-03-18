from crs import MagnaSirgasCRS
from pyproj import CRS


class Ellipsoidal(MagnaSirgasCRS):
    _max_north = 90.0
    _min_south = -90.0
    _max_east = 180.0
    _min_west = -180.0
    _crs_type = "Ellipsoidal"

    @classmethod
    def name_from_proj(self):
        pass


class IntHayford1924(Ellipsoidal):
    _crs = CRS.from_user_input("+proj=longlat +ellps=intl")
    _proj_name = "intl"

    def __init__(self):
        pass

    def name_from_prj(self):
        return self._proj_name

    def crs(cls):
        return cls._crs

    def max_north(self):
        return self._max_north

    def min_south(self):
        return self._min_south

    def max_east(self):
        return self._max_east

    def min_west(self):
        return self._min_west

    def __hash__(self) -> int:
        return hash(self._crs)

    def __eq__(self, __value: object) -> bool:
        return self._crs == __value._crs

    def __repr__(self):
        return f"IntHayford()"

    def __str__(self) -> str:
        return f"IntHayford1924 is {IntHayford1924._crs_type} coming from PROJ ({IntHayford1924._crs}) with limits in longitude ({self.max_east(), self.min_west()} and in latitude ({self.max_north(), self.min_south()}))"


class IntHayford1924(Ellipsoidal):
    _crs = CRS.from_user_input("+proj=longlat +ellps=wgs84")
    _proj_name = "wgs84"

    def __init__(self):
        pass

    def name_from_prj(self):
        return self._proj_name

    def crs(cls):
        return cls._crs

    def max_north(self):
        return self._max_north

    def min_south(self):
        return self._min_south

    def max_east(self):
        return self._max_east

    def min_west(self):
        return self._min_west

    def __hash__(self) -> int:
        return hash(self._crs)

    def __eq__(self, __value: object) -> bool:
        return self._crs == __value._crs

    def __repr__(self):
        return f"IntHayford()"

    def __str__(self) -> str:
        return f"IntHayford1924 is {IntHayford1924._crs_type} coming from PROJ ({IntHayford1924._crs}) with limits in longitude ({self.max_east(), self.min_west()} and in latitude ({self.max_north(), self.min_south()}))"
