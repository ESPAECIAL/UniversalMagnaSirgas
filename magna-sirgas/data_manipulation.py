import logging

import numpy as np

from abc import ABC
from crs import MagnaSirgasCRS

logging.basicConfig(level=logging.DEBUG)

class SimpleAdapter(ABC):

    # The column index in an array
    COL_ARRAY   = 1
    # floats for a projected coordinate in two dimensions
    COORDS_2D   = 2
    # Numpy type for the 64 bytes float
    DTYPE_64    = np.dtype(np.float64).type
    # Numpy type for the 32 bytes float
    DTYPE_32    = np.dtype(np.float32).type
    NAME        = "SimpleColombianTransformer"

    def __repr__(self) -> str:
        return f"{self.NAME}({self.crs1}, {self.crs2})"
    
    def __str__(self) -> str:
        return f"{self.NAME}"
    
    def exchanges_crs(self):
        temp      = self.crs1
        self.crs1 = self.crs2
        self.crs2 = temp

    def _is_magnasirgascrs_subclass(self, crs):
        return isinstance(crs, MagnaSirgasCRS)
    
    def _are_crs_magnasirgascrs_subclasses(self, *many_crs):
        for crs in many_crs:
            if not self._is_magnasirgascrs_subclass(crs): return False
        return True
    
    def _which_are_not_magnasirgascrs_subclasses(self, *manycrs):
        not_magnasirgas_crs = list()
        for crs in manycrs:
            if not self._is_magnasirgascrs_subclass(crs): not_magnasirgas_crs.append(crs)
        return tuple(not_magnasirgas_crs)
    
    def _origin_target_arenot_magnasirgascrs_log(self, crs1, crs2):
        t  = self._which_are_not_magnasirgascrs_subclasses(crs1, crs2)
        print(t)
        logging.error(f"{t} are not subclasses of {MagnaSirgasCRS}")
        raise KeyError(f"{t} are not subclasses of {MagnaSirgasCRS}")