from crs import MagnaSirgasCRS
from pyproj import CRS

class Ellipsoidal(MagnaSirgasCRS):
    _max_north  = 90.0
    _min_south  = -90.0
    _max_east   = 180.0
    _min_west   = -180.0
    _type       = "Ellipsoidal"
    @classmethod
    def type(cls):
        return cls._type
    @classmethod
    def max_north(cls):
        return cls._max_north
    @classmethod
    def min_south(cls):
        return cls._min_south
    @classmethod
    def max_east(cls):
        return cls._max_east
    @classmethod
    def min_west(cls):
        return cls._min_west
    @classmethod
    def crs(self):
        pass
    @classmethod
    def name_from_proj(self):
        pass

class IntHayford1924(Ellipsoidal):
    def __init__(self):
        self._crs       = CRS.from_user_input("+proj=longlat +ellps=intl")
        self._proj_name = 'intl'
    def max_north(self):
        return self._max_north
    def min_south(self):
        return self._min_south
    def max_east(self):
        return self._max_east
    def min_west(self):
        return self._min_west
    def crs(self):
        return self._crs
    def proj_name(self):
        return self._proj_name
    def __hash__(self) -> int:
        return hash(self._crs)
    def __eq__(self, __value: object) -> bool:
        return self._crs == __value._crs
    def __repr__(self):
        return f"EPSG21897() have the crs {self.crs}"
    def __str__(self) -> str:
        return f"IntHayford1824 is {IntHayford1924.type} with limits in longitude ({self._max_east}, {self._min_west} and in latitude ({self._max_north, self._min_south}))"