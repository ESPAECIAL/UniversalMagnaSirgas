from crs import MagnaSirgasCRS
from pyproj import CRS

class Projected(MagnaSirgasCRS):
    _crs_type = "Projected"

class EPSG21897(Projected):
    """The ranges of this must be adjusted
    """
    _crs        = CRS.from_user_input(21897)
    _max_north  = 1799074.0
    _min_south  = 213804.0
    _max_east   = 1163585.2414666042
    _min_west   = 832143.631295867

    def __init__(self):
        pass

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
        return f"EPSG21897() have the crs {self.crs()}"
    
    def __str__(self) -> str:
        return f"EPSG21897 is {EPSG21897._crs_type} coming from PROJ ({EPSG21897._crs}) with limits in east ({self.max_east()}, {self.min_west()} and in north ({self.max_north(), self.min_south()}))"