import logging
import numpy as np
from typing import Union, Type
from abc import ABC, abstractmethod
from crs import MagnaSirgasCRS
from projected_crs import EPSG21897, Projected
from geographic_crs import Ellipsoidal
from pyproj import Proj, Transformer

logging.basicConfig(level=logging.DEBUG)

class SimpleColombianTransformer(ABC):
    # The column index in an array
    COL_ARRAY   = 1
    # floats for a projected coordinate in two dimensions
    COORDS_2D   = 2
    # Numpy type for the 64 bytes float
    DTYPE_64    = np.dtype(np.float64).type
    # Numpy type for the 32 bytes float
    DTYPE_32    = np.dtype(np.float32).type
    NAME        = "SimpleColombianTransformer"
    def __init__(self):
        pass
    def __repr__(self) -> str:
        return f"{self.NAME}({self.origin}, {self.target})"
    def __str__(self) -> str:
        return f"{self.NAME}"
    @abstractmethod
    def exhanges_crs(self):
        temp        = self.target
        self.origin = self.target
        self.target = temp
    @abstractmethod
    def _is_magnasirgascrs_subclass(self, crs):
        return issubclass(crs, MagnaSirgasCRS)
    @abstractmethod
    def _are_magnasirgascrs_subclasses(self, *many_crs):
        for crs in many_crs:
            if not self._is_magnasirgascrs_subclass(crs): return False
    @abstractmethod
    def _which_are_not_magnasirgascrs_subclasses(self, *many_crs):
        not_magnasirgas_crs = list()
        for crs in many_crs:
            if not self._is_magnasirgascrs_subclass(crs): not_magnasirgas_crs.append(crs)
        return tuple(not_magnasirgas_crs)
    @abstractmethod
    def _origin_target_setter(self, origin_crs, target_crs):
        self.origin = origin_crs
        self.target = target_crs
    @abstractmethod
    def _origin_target_log(self, origin_crs, target_crs):
        logging.error(f"{self._which_are_not_magnasirgascrs_subclasses(origin_crs, target_crs)} are not subclasses of {MagnaSirgasCRS}")
    @abstractmethod
    def origin_target(self, origin_crs, target_crs):
        if self._are_magnasirgascrs_subclasses(origin_crs, target_crs):
            self._origin_target_setter(origin_crs, target_crs)
        else:
            self._origin_target_log(origin_crs, target_crs)

class Projection(SimpleColombianTransformer):
    COORDINATE_TYPES = ("Projected", "Geographic")
    def __init__(self):
        print("Projection between %s and %s coordinates" % self.COORDINATE_TYPES)
    @abstractmethod
    def validates_coordinate_types(self):
        crs_types   = (self.origin, self.target)
        match crs_types:
            case (Ellipsoidal(), Projected()): return True
            case (Projected(), Ellipsoidal()): return True
            case _: return False
    @abstractmethod
    def organizes_coordinatetype_direction(self, proj_to_geog: bool):
        if self.validates_coordinate_types():
            crs_types   = (self.origin, self.target)
            match crs_types:
                case (Ellipsoidal(), Projected()) if proj_to_geog:
                    self.exchanges_crs()
                case (Projected(), Ellipsoidal()) if not proj_to_geog:
                    self.exchanges_crs()
                case _: pass

    @abstractmethod
    def _differentiates_input_patterns(self, proj, inverse):
        match coords:
            case (float(x), float(y)) if (x >= self.origin.MINIMUM_X and x < self.origin.MAXIMUM_X) \
                and (y >= self.origin.MINIMUM_Y and y < self.origin.MAXIMUM_Y):
                return proj(coords, inverse=inverse)
            case np.array(coords) if isinstance(coords.dtype, np.array) and coords.shape[self.COL_ARRAY] == self.COORDS_2D \
                and (coords.dtype == self.DTYPE_64 or coords.dtype == self.DTYPE_32):
                return proj(coords, inverse=inverse)
            case _:
                # This should be corrected to add the real ranges of EPSG21897
                logging.error(f"Invalid coordinates: {coords}. They should be in a tuple of floats (x, y) or in a type readable for numpy.array() and within the range")
    
    @abstractmethod
    def projects_projected_to_geographic(self, coords):
        self.organize_order_projection(proj_to_geog=True)
        proj     = Proj(self.origin.crs(), ellps=self.target.name_from_proj())
        return self._differentiates_input_patterns(self, proj, True)
    
    @abstractmethod
    def projects_geographic_to_projected(self, coords):
        self.organize_order_projection(proj_to_geog=False)
        proj     = Proj(self.origin.crs(), ellps=self.target.name_from_proj())
        return self._differentiates_input_patterns(self, proj, False)

class EPSG21897_INTL1924_Projector(Projection):
    CRSs = ("EPSG21897", "Hayford International 1294")
    STR_REPRESENTATION = "With %s and %s" % CRSs
    def __init__(self):
        super().__init__()
        print(self.STR_REPRESENTATION + " started")
    def __str__(self) -> str:
        return self.STR_REPRESENTATION
    
if __name__ == "__main__":
    import numpy as np
    coords      =   (968262.8, 1062237.1)
    many_coords =   ((969767.2, 1060687.6),
                    (969315.3, 1061151.8),
                    (968964.5, 1061513.4),
                    (968638.5, 1061849.5),
                    (968262.8, 1062237.1),
                    (968262.8, 1062237.1),
                    (967910.1, 1062596.9),
                    (967560.5, 1062959.8),
                    (967209, 1063321.2),
                    (966858.1, 1063682.9),
                    (966531.6, 1064018),
                    (966180.4, 1064379.4),
                    (965804.4, 1064766.7),
                    (965477.8, 1065101.9),
                    (965100.9, 1065488.6),
                    (964749.4, 1065849.7),
                    (964449.8, 1066160.8),
                    (964130.6, 1066490.4),
                    (964049, 1066574.4),
                    (963698.1, 1066936.1),
                    (963346.7, 1067297.8),
                    (963020.4, 1067633.3),
                    (962644.4, 1068020.9),
                    (962293, 1068382.3),
                    (961892.1, 1068795.9),
                    (961591, 1069105.8),
                    (961277.6, 0.0))
    many_coords =   np.array(many_coords)
    print(many_coords[0])
    coltrans    = ColombianTransformer()
    wgs84       = coltrans.from_epsg21897_to_hayford_intl(many_coords)
    print(wgs84)
    # print("%.7f, %.7f" % wgs84)  # Adjust the format specifier accordingly