import logging

from pyproj import Transformer

from data_manipulation import SimpleAdapter
from geographic_crs import Ellipsoidal, IntHayford1924, WGS1984


class TransformerGG(SimpleAdapter):
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

        from pyproj import Transformer

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


class WGS84_INTLHAYFORD1924_T(TransformerGG):
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

    # from transformations import WGS84_INTLHAYFORD1924_T
    # import numpy as np

    # many_coords = (
    #     (969767.2, 1060687.6),
    #     (969315.3, 1061151.8),
    #     (968964.5, 1061513.4),
    #     (968638.5, 1061849.5),
    #     (968262.8, 1062237.1),
    #     (968262.8, 1062237.1),
    #     (967910.1, 1062596.9),
    #     (967560.5, 1062959.8),
    #     (967209, 1063321.2),
    #     (966858.1, 1063682.9),
    #     (966531.6, 1064018),
    #     (966180.4, 1064379.4),
    #     (965804.4, 1064766.7),
    #     (965477.8, 1065101.9),
    #     (965100.9, 1065488.6),
    #     (964749.4, 1065849.7),
    #     (964449.8, 1066160.8),
    #     (964130.6, 1066490.4),
    #     (964049, 1066574.4),
    #     (963698.1, 1066936.1),
    #     (963346.7, 1067297.8),
    #     (963020.4, 1067633.3),
    #     (962644.4, 1068020.9),
    #     (962293, 1068382.3),
    #     (961892.1, 1068795.9),
    #     (961591, 1069105.0),
    #     (961277.6, 1069428.7),
    # )
    # coltrans = WGS84_INTLHAYFORD1924_T()
    # coltrans.transforms_straightforwardly(many_coords)
