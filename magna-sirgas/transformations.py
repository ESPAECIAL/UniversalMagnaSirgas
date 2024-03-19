import logging

from pyproj import CRS, Transformer

from data_manipulation import SimpleAdapter
from geographic_crs import Ellipsoidal


class Transformer(SimpleAdapter):
    COORD_TYPES = ("Geographic", "Geographic")

    def __init__(self, crs1, crs2):
        if self._validates_coord_types(crs1, crs2):
            self.crs1 = crs1
            self.crs2 = crs2
            print("Transformation between %s and %s coords" % self.COORD_TYPES)
        else:
            return logging.error(
                f"The crs' {crs1, crs2} do not create a pipeline to transform"
            )

    def _validates_coord_types(self, crs1, crs2):
        if super()._validates_coord_types(crs1, crs2):
            if isinstance(crs1, Ellipsoidal) and isinstance(crs2, Ellipsoidal):
                return True
        return False

    def transforms(self, coords):
        self.error_message = []
        self.warning_message = []
        self.transformation = Transformer.from_crs(self.crs1._crs, self.crs2._crs, always_xy=True)
        self._differentiates_input_patterns(coords, False)
    
    def get_results(self):



# intl = CRS.from_user_input("+proj=longlat +ellps=intl")
# wgs84 = CRS.from_user_input("+proj=longlat +ellps=WGS84")
