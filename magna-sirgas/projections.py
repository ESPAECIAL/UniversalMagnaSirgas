import logging

import numpy as np
from pyproj import Proj

from data_manipulation import SimpleAdapter
from projected_crs import EPSG21897, Projected
from geographic_crs import Ellipsoidal, IntHayford1924

class Projecter(SimpleAdapter):

    COORDINATE_TYPES = ("Projected", "Geographic")

    def __init__(self, crs1, crs2):
        if self.validates_coordinate_types(crs1, crs2):
            self.crs1 = crs1
            self.crs2 = crs2
        else:
            self._origin_target_log(crs1, crs2)
        print("Projection between %s and %s coordinates" % self.COORDINATE_TYPES)
    
    def get_results(self):
        return self.results
    
    def projects_geographic_to_projected(self, coords):
        self.organizes_coordinatetype_pipeline(proj_to_geog=False)
        self.proj   = Proj(self.crs1._crs(), ellps=self.crs2.name_from_proj())
        self._differentiates_input_patterns(coords, False)
    
    def projects_projected_to_geographic(self, coords):
        self.organizes_coordinatetype_pipeline(proj_to_geog=True)
        self.proj   = Proj(self.crs1._crs, ellps=self.crs2.name_from_proj())
        self._differentiates_input_patterns(coords, True)
    
    def _differentiates_input_patterns(self, coords, inverse):
        match coords:
            case (float(east), float(north)) if self._validates_boundaried_single_paired_coordinates(east, north):
                self.results = self.proj(coords, inverse=inverse)
            case ((float(), float()), *_ , (float(), float())) if isinstance(coords, tuple) and self._validates_2d_tuple(coords):
                coords  = np.array(coords)
                coords  = coords.transpose()
                self.results = self.proj(tuple(coords[0]), tuple(coords[1]), inverse=inverse)
            case _:
                # This should be corrected to add the real ranges of EPSG21897
                logging.error(f"Invalid coordinates: {coords}. They should be in a tuple of floats (x, y) or in a type readable for numpy.array() and within the range")

    def organizes_coordinatetype_pipeline(self, proj_to_geog: bool):
        if isinstance(self.crs1, Ellipsoidal) and isinstance(self.crs2, Projected) and proj_to_geog: self.exchanges_crs()
        if isinstance(self.crs1, Projected) and isinstance(self.crs2, Ellipsoidal) and not proj_to_geog: self.exchanges_crs()

    def validates_coordinate_types(self, crs1, crs2):
        if isinstance(crs1, Ellipsoidal) and isinstance(crs2, Projected): return True
        if isinstance(crs1, Projected) and isinstance(crs2, Ellipsoidal): return True
        self._origin_target_arenot_projectable_log(crs1, crs2)
    
    def _origin_target_arenot_projectable_log(self, crs1, crs2):
        return logging.error(f"The crs' {crs1, crs2} dont create a pipeline to project")

    def _validates_boundaried_single_paired_coordinates(self, e, n):
        e_is_well_boundaried = (e >= self.crs1._min_west and e < self.crs1._max_east)
        n_is_well_boundaried = (n >= self.crs1._min_south and n < self.crs1._max_north)
        return e_is_well_boundaried and n_is_well_boundaried
    
    def _validates_2d_tuple(self, coords):
        cond1   = self._validates_boundaried_paired_coordinates(coords)
        cond2   = self._validates_tuple_as_float_container(coords)
        return cond1 and cond2
    
    def _validates_boundaried_paired_coordinates(self, coords):
        arr_coords  = np.array(coords).transpose()
        e_coords    = arr_coords[0]
        n_coords    = arr_coords[1]
        e_is_well_boundaried = (min(e_coords) >= self.crs1._min_west and max(e_coords) < self.crs1._max_east)
        n_is_well_boundaried = (min(n_coords) >= self.crs1._min_south and max(n_coords) < self.crs1._max_north)
        return e_is_well_boundaried and n_is_well_boundaried
    
    def _validates_tuple_as_float_container(self, coords):
        is_always_bidimensional = np.array(coords).shape[self.COL_ARRAY] == self.COORDS_2D
        is_float                = (np.array(coords).dtype == self.DTYPE_64 or np.array(coords).dtype == self.DTYPE_32)
        return is_always_bidimensional and is_float
        
    
class EPSG21897_INTL1924_Projector(Projecter):

    CRSs = ("EPSG21897", "Hayford International 1924")
    STR_REPRESENTATION = "With %s and %s" % CRSs

    def __init__(self, crs1, crs2):
        super().__init__(crs1, crs2)
        print(self.STR_REPRESENTATION + " started")

    def __str__(self) -> str:
        return self.STR_REPRESENTATION

    def organizes_coordinatetype_direction(self, proj_to_geog: bool):
        super().organizes_coordinatetype_direction(proj_to_geog)

    def _differentiates_input_patterns(self, proj, inverse):
        super()._differentiates_input_patterns(proj, inverse)

    def projects_projected_to_geographic(self, coords):
        super().projects_projected_to_geographic(coords)

    def projects_geographic_to_projected(self, coords):
        super().projects_geographic_to_projected(coords)
    
    def get_results(self):
        return super().get_results()
    
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
                    (961591, 1069105.0),
                    (961277.6, 1.0))

    coltrans    = EPSG21897_INTL1924_Projector(IntHayford1924(), EPSG21897())
    coltrans.projects_projected_to_geographic(many_coords)
    print(coltrans.get_results())
    # print("%.7f, %.7f" % wgs84)  # Adjust the format specifier accordingly