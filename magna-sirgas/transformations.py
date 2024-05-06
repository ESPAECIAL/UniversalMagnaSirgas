import logging

from pyproj import Transformer

from data_manipulation import SimpleAdapter
from geographic_crs import Ellipsoidal, IntHayford1924, WGS1984


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

    def transforms_straightforwardly(self, coords):
        self.error_message = []
        self.warning_message = []
        self.transformation = Transformer.from_crs(
            self.crs1._crs, self.crs2._crs, always_xy=True
        )
        self._differentiates_input_patterns(
            coords, functional="elipsoidal-transformation"
        )

    def transforms_inversely(self, coords):
        self.error_message = []
        self.warning_message = []
        self.transformation = Transformer.from_crs(
            self.crs2._crs, self.crs1._crs, always_xy=True
        )
        self._differentiates_input_patterns(
            coords, functional="elipsoidal-transformation"
        )


class WGS84_INTLHAYFORD1924_T(Transformer):
    CRSs = (
        "WGS84 (EPSG:4326)",
        "Hayford International 1909 (EPSG:7022)",
    )

    STR_REPRESENTATION = "With %s and %s" % CRSs

    def __init__(self):
        super().__init__(WGS1984(), IntHayford1924())
        print(self.STR_REPRESENTATION + " started")

    def __str__(self) -> str:
        return self.STR_REPRESENTATION


if __name__ == "__main__":
    import doctest

    doctest.testfile("transformations_tests.txt")
