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
        error_message = None
        match coords:

            case (float(east), float(north)) if self._validates_boundaried_single_paired_coordinates(east, north):
                self.results    = self.proj(east, north, inverse=inverse)

            case (float(east), float(north)) if not self._validates_boundaried_single_paired_coordinates(east, north):
                error_message   = f"Coordinates are not within the crs boundaries"
                self.results    = self.proj(east, north, inverse=inverse)

            case (int(east), int(north)) if self._validates_boundaried_single_paired_coordinates(east, north):
                error_message   = f"Coordinates are integers and are not within the crs boundaries, be cautios"
                self.results    = self.proj(east, north, inverse=inverse)

            case (int(east), int(north)) if not self._validates_boundaried_single_paired_coordinates(east, north):
                error_message   = f"Coordinates are integers, be cautios. "
                self.results    = self.proj(east, north, inverse=inverse)
            
            case (east, north) if self._are_transformable_from_string_to_numerical(east, north):
                float_e, float_n= self._transforms_single_string_coordinates_to_numerical(coords)
                self.results    = self.proj(float_e, float_n, inverse=inverse)
            
            case (east, north) if not self._are_transformable_from_string_to_numerical(east, north):
                error_message   = f"Coordinates can not transformed to floats."

            case ((float(), float()), *_ , (float(), float())) if isinstance(coords, tuple) and self._validates_2d_tuple(coords):
                coords          = np.array(coords)
                coords          = coords.transpose()
                self.results    = self.proj(tuple(coords[0]), tuple(coords[1]), inverse=inverse)

            case ((float(), float()), *_ , (float(), float())) if isinstance(coords, tuple) and not self._validates_is_always_bidimensional(coords):
                self.results    = None
                error_message   = f"Coordinates do not come always paired"
                ## Write method to make the user know where are the not well paired coordinates

            case ((float(), float()), *_ , (float(), float())) if isinstance(coords, tuple) and not self._validates_tuple_as_float_container(coords):
                self.results    = None
                error_message   = f"The coordinates are not all floats"

            case ((float(), float()), *_ , (float(), float())) if isinstance(coords, tuple) and not self._validates_boundaried_paired_coordinates(coords):
                self.results    = self.proj(tuple(coords[0]), tuple(coords[1]), inverse=inverse)
                error_message   = f"Coordinates are not within the crs boundaries"
            
            case ((east1, north1), *_, (eastn, northn)) if self._are


            case _:
                self.results    = None
                error_message   = f"Invalid coordinates. They all should be floats"

        if error_message:
            print(error_message)

    def organizes_coordinatetype_pipeline(self, proj_to_geog: bool):
        if isinstance(self.crs1, Ellipsoidal) and isinstance(self.crs2, Projected) and proj_to_geog: self.exchanges_crs()
        if isinstance(self.crs1, Projected) and isinstance(self.crs2, Ellipsoidal) and not proj_to_geog: self.exchanges_crs()

    def validates_coordinate_types(self, crs1, crs2):
        if isinstance(crs1, Ellipsoidal) and isinstance(crs2, Projected): return True
        if isinstance(crs1, Projected) and isinstance(crs2, Ellipsoidal): return True
        self._origin_target_arenot_projectable_log(crs1, crs2)

    def _origin_target_arenot_projectable_log(self, crs1, crs2):
        return logging.error(f"The crs' {crs1, crs2} do not create a pipeline to project")

    def _validates_boundaried_single_paired_coordinates(self, e, n):
        e_is_well_boundaried = (e >= self.crs1._min_west and e < self.crs1._max_east)
        n_is_well_boundaried = (n >= self.crs1._min_south and n < self.crs1._max_north)
        return e_is_well_boundaried and n_is_well_boundaried
    
    def _validates_2d_tuple(self, coords):
        cond1   = self._validates_is_always_bidimensional(coords)
        cond2   = self._validates_boundaried_paired_coordinates(coords)
        cond3   = self._validates_tuple_as_float_container(coords)
        return cond1 and cond2
    
    def _validates_boundaried_paired_coordinates(self, coords):
        arr_coords  = np.array(coords).transpose()
        e_coords    = arr_coords[0]
        n_coords    = arr_coords[1]
        e_is_well_boundaried = (min(e_coords) >= self.crs1._min_west and max(e_coords) < self.crs1._max_east)
        n_is_well_boundaried = (min(n_coords) >= self.crs1._min_south and max(n_coords) < self.crs1._max_north)
        return e_is_well_boundaried and n_is_well_boundaried
    
    def _validates_is_always_bidimensional(self, coords):
        return np.array(coords).shape[self.COL_ARRAY] == self.COORDS_2D

    def _validates_tuple_as_float_container(self, coords):
        return np.array(coords).dtype == self.DTYPE_64 or np.array(coords).dtype == self.DTYPE_32

    def _transforms_from_2d_string_tuple_to_numerical(self, coords):
        float_coordinates = []
        for coord in coords:
            float_coordinates.append(self._transforms_single_string_coordinates_to_numerical(coord))
        return tuple(float_coordinates)

    def _transforms_single_string_coordinates_to_numerical(self, coords):
        return float(coords[0]), float(coords[1])

    def _shows_not_transformable_float_from_single_coordinates(self, coords):
        not_float_transformable = []
        for coord in coords:
            if self._is_transformable_from_string_to_numerical(coord): not_float_transformable.append(coord)
        return tuple(not_float_transformable)
    
    def _shows_not_float_coordinates_from_2d_tuple(self, coords):
        not_float_transformable = []
        for coord, row in enumerate(coords):
            if not self._are_transformable_from_string_to_numerical(coord):
                not_float_transformable.append((row, coords))
        return not_float_transformable

    def _are_transformable_from_string_to_numerical(self, *coords):
        for coord in coords:
            if not self._is_transformable_from_string_to_numerical(coord): return False
        return True

    def _is_transformable_from_string_to_numerical(self, coord):
        _is_transformable = False
        try:
            float(coord)
            _is_transformable = True
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return _is_transformable


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
        """
        >>> import numpy as np
        >>> coords      =   (968262.8, 1062237.1)
        >>> many_coords =   ((969767.2, 1060687.6),
        ...                 (969315.3, 1061151.8),
        ...                 (968964.5, 1061513.4),
        ...                 (968638.5, 1061849.5),
        ...                 (968262.8, 1062237.1),
        ...                 (968262.8, 1062237.1),
        ...                 (967910.1, 1062596.9),
        ...                 (967560.5, 1062959.8),
        ...                 (967209, 1063321.2),
        ...                 (966858.1, 1063682.9),
        ...                 (966531.6, 1064018),
        ...                 (966180.4, 1064379.4),
        ...                 (965804.4, 1064766.7),
        ...                 (965477.8, 1065101.9),
        ...                 (965100.9, 1065488.6),
        ...                 (964749.4, 1065849.7),
        ...                 (964449.8, 1066160.8),
        ...                 (964130.6, 1066490.4),
        ...                 (964049, 1066574.4),
        ...                 (963698.1, 1066936.1),
        ...                 (963346.7, 1067297.8),
        ...                 (963020.4, 1067633.3),
        ...                 (962644.4, 1068020.9),
        ...                 (962293, 1068382.3),
        ...                 (961892.1, 1068795.9),
        ...                 (961591, 1069105.0),
        ...                 (961277.6, 1069428.7))
        >>> coltrans    = EPSG21897_INTL1924_Projector(IntHayford1924(), EPSG21897())
        Projection between Projected and Geographic coordinates
        With EPSG21897 and Hayford International 1924 started
        >>> coltrans.projects_projected_to_geographic(many_coords)
        >>> print(coltrans.get_results())
        ((-74.35358325591312, -74.35766067985358, -74.36082593598195, -74.36376745189135, -74.36715744943729, -74.36715744943729, -74.37033993174022, -74.37349450015495, -74.3766662311776, -74.37983258452327, -74.38277878699914, -74.38594790763798, -74.38934085364151, -74.39228804928436, -74.39568917997471, -74.39886113795443, -74.40156478805952, -74.40444533036123, -74.40518171275346, -74.40834835991517, -74.41151954964633, -74.41446425347509, -74.41785751628629, -74.42102880304505, -74.42464685994848, -74.42736425877526, -74.43019269941865), (5.147783032413364, 5.151978921584383, 5.155247396947399, 5.158285363956912, 5.161788815052751, 5.161788815052751, 5.165040952014809, 5.16832111624766, 5.171587690516878, 5.174856962089231, 5.177885784023651, 5.181152306618579, 5.184652908484098, 5.187682583685979, 5.191177716947414, 5.194441451327794, 5.197253270266719, 5.200232275194031, 5.200991484034273, 5.204260592031021, 5.207529679342289, 5.210561949822666, 5.214065088356036, 5.217331407607902, 5.221069491958975, 5.223863090340863, 5.226788636343087))
        >>> coltrans.projects_projected_to_geographic(coords)
        >>> print(coltrans.get_results())
        (-74.36715744943729, 5.161788815052751)
        >>> coltrans.projects_projected_to_geographic(('a', 'b'))
        Invalid coordinates: ('a', 'b'). They should be in a tuple of floats (x, y) or in a type readable by numpy.array() and within the range
        >>> coltrans.projects_projected_to_geographic(('a', 0))
        Invalid coordinates: ('a', 0). They should be in a tuple of floats (x, y) or in a type readable by numpy.array() and within the range
        >>> coltrans.projects_projected_to_geographic((1, 0))
        Invalid coordinates: (1, 0). They should be in a tuple of floats (x, y) or in a type readable by numpy.array() and within the range
        >>> print(coltrans.get_results())
        None
        """
        super().projects_projected_to_geographic(coords)

    def projects_geographic_to_projected(self, coords):
        super().projects_geographic_to_projected(coords)
    
    def get_results(self):
        return super().get_results()
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # print("%.7f, %.7f" % wgs84)  # Adjust the format specifier accordingly