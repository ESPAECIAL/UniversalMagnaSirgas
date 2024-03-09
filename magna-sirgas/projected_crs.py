from crs import MagnaSirgasCRS
from pyproj import CRS

class Projected(MagnaSirgasCRS):
    _type = "Projected"
    @classmethod
    def type(cls):
        return cls._type

class EPSG21897(MagnaSirgasCRS):
    """The ranges of this must be adjusted
    """
    def __init__(self):
        self._max_north  = 1069428.8
        self._min_south  = 1060687.5
        self._max_east   = 969767.3
        self._min_west   = 961277.5
        self._crs        = CRS.from_user_input(21897)
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
    def __hash__(self) -> int:
        return hash(self._crs)
    def __eq__(self, __value: object) -> bool:
        return self._crs == __value._crs
    def __repr__(self):
        return f"EPSG21897() have the crs {self.crs}"
    def __str__(self) -> str:
        return f"EPSG21897 is {EPSG21897.type} with limits in east ({self._max_east}, {self._min_west} and in north ({self._max_north, self._min_south}))"