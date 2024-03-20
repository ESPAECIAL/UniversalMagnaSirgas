import logging

import numpy as np

from pyproj import Proj
from abc import abstractmethod

from data_manipulation import SimpleAdapter
from projected_crs import Projected, EPSG21897
from geographic_crs import Ellipsoidal, IntHayford1924


class Projecter(SimpleAdapter):

    COORD_TYPES = ("Projected", "Geographic")

    def __init__(self, crs1, crs2):
        if self._validates_coord_types(crs1, crs2):
            self.crs1 = crs1
            self.crs2 = crs2
            print("Projection between %s and %s coords" % self.COORD_TYPES)
        else:
            return logging.error(
                f"The crs' {crs1, crs2} do not create a pipeline to project"
            )

    def _validates_coord_types(self, crs1, crs2):
        if super()._validates_coord_types(crs1, crs2):
            return (
                (isinstance(crs1, Ellipsoidal) and isinstance(crs2, Projected))
                or isinstance(crs1, Projected)
                and isinstance(crs2, Ellipsoidal)
            )
        else:
            self._log_origin_target_arenot_projectable(crs1, crs2)
            return False

    def projects_geographic_to_projected(self, coords):
        self.error_message = []
        self.warning_message = []
        self.organizes_coordtype_pipeline(proj_to_geog=False)
        self.projection = Proj(self.crs2._crs, ellps=self.crs1.name_from_proj())
        self._differentiates_input_patterns(coords, functional="forward-projection")

    def projects_projected_to_geographic(self, coords):
        self.error_message = []
        self.warning_message = []
        self.organizes_coordtype_pipeline(proj_to_geog=True)
        self.projection = Proj(self.crs1._crs, ellps=self.crs2.name_from_proj())
        self._differentiates_input_patterns(coords, functional="inverse-projection")

    def organizes_coordtype_pipeline(self, proj_to_geog: bool):
        if (
            isinstance(self.crs1, Ellipsoidal)
            and isinstance(self.crs2, Projected)
            and proj_to_geog
        ):
            self.exchanges_crs()
        if (
            isinstance(self.crs1, Projected)
            and isinstance(self.crs2, Ellipsoidal)
            and not proj_to_geog
        ):
            self.exchanges_crs()


class EPSG21897_INTL1924_P(Projecter):

    CRSs = (
        "Bogota 1975 / Colombia Bogota zone (EPSG:21897)",
        "Hayford International 1909 (EPSG:7022)",
    )

    STR_REPRESENTATION = "With %s and %s" % CRSs

    def __init__(self):
        super().__init__(IntHayford1924(), EPSG21897())
        print(self.STR_REPRESENTATION + " started")

    def __str__(self) -> str:
        return self.STR_REPRESENTATION


if __name__ == "__main__":
    import doctest

    doctest.testfile("projections_tests.txt")
