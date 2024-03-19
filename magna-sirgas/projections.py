import logging

import numpy as np

from pyproj import Proj
from abc import abstractmethod

from data_manipulation import SimpleAdapter
from projected_crs import Projected
from geographic_crs import Ellipsoidal


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

    def get_results(self):
        return self.results

    @abstractmethod
    def projects_geographic_to_projected(self, coords):
        self.error_message = []
        self.warning_message = []
        self.organizes_coordtype_pipeline(proj_to_geog=False)
        self.projection = Proj(self.crs2._crs, ellps=self.crs1.name_from_proj())
        self._differentiates_input_patterns(coords, False)

    @abstractmethod
    def projects_projected_to_geographic(self, coords):
        self.error_message = []
        self.warning_message = []
        self.organizes_coordtype_pipeline(proj_to_geog=True)
        self.projection = Proj(self.crs1._crs, ellps=self.crs2.name_from_proj())
        self._differentiates_input_patterns(coords, True)

    @abstractmethod
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

    @abstractmethod
    def _differentiates_input_patterns(self, coords, inverse):
        self._matches_single_2d_coords(coords, inverse)
        if not self._coords_are_single_paired:
            self._matches_not_single_2d_coords(coords, inverse)
        self._prints_final_message()

    def _has_messages(self):
        return self._has_error_message() or self._has_warning_message()

    def _prints_final_message(self):
        if self._has_warning_message():
            print(" ".join(self.warning_message).strip())
        if self._has_error_message():
            print(" ".join(self.error_message).strip())
        else:
            print("Successfull")

    def _has_error_message(self):
        if len(self.error_message) != 0:
            self.error_message.insert(0, f"{len(self.error_message)} Error(s):")
            return True
        return False

    def _has_warning_message(self):
        if len(self.warning_message) != 0:
            self.warning_message.insert(0, f"{len(self.warning_message)} Warning(s):")
            return True
        return False

    def _prints_error_message(self):
        return len(self.error_message) != 0

    def _prints_warning_message(self):
        return len(self.warning_message) != 0

    def _matches_single_2d_coords(self, coords, inverse):
        self._coords_are_single_paired = True
        match coords:
            case (
                float(east),
                float(north),
            ) if self._validates_boundaried_single_paired_coords(east, north):
                self.results = self.projection(east, north, inverse=inverse)

            case (
                float(east),
                float(north),
            ) if not self._validates_boundaried_single_paired_coords(east, north):
                self.Warning_message.append(
                    "Coordinates are not all within the crs boundaries."
                )
                self.results = self.projection(east, north, inverse=inverse)

            case (east, north) if self._validates_are_transformable_to_float(
                east, north
            ):
                float_e, float_n = self._transforms_single_coords_to_float(coords)
                self.warning_message.append("Coordinates were transform to floats.")
                if not self._validates_boundaried_single_paired_coords(east, north):
                    self.warning_message.append(
                        "Coordinates are not all within the crs boundaries."
                    )
                self.results = self.projection(float_e, float_n, inverse=inverse)

            case (east, north) if not self._validates_are_transformable_to_float(
                east, north
            ):
                self.error_message.append(
                    "Coordinates can not be transformed to floats."
                )
                self.results = None
            case _:
                self._coords_are_single_paired = False

    def _matches_not_single_2d_coords(self, coords, inverse):
        match coords:

            case (
                (east1, north1),
                *_,
                (eastn, northn),
            ) if self._validates_2d_float_sequence_boundaried_coordinates(coords):
                narrays_coords = self._2d_iterable_to_narray(coords)
                self.results = self.projection(*narrays_coords, inverse=inverse)

            case (
                (east1, north1),
                *_,
                (eastn, northn),
            ) if self._validates_2d_float_transformable(coords):
                coords = np.array(self._transforms_2d_tuple_to_float(coords))
                self.warning_message += [
                    "Coordinates were not all floats, but transformed to floats.",
                    "Coordinatess are not all within the crs boundaries.",
                ]
                narrays_coords = self._2d_iterable_to_narray(coords)
                self.results = self.projection(*narrays_coords, inverse=inverse)

            case (
                (east1, north1),
                *_,
                (eastn, northn),
            ) if not self._validates_is_iterable(coords):
                self.error_message.append(
                    "The object for the coordinates is not iterable."
                )

            case (
                (east1, north1),
                *_,
                (eastn, northn),
            ) if not self._validates_is_always_2d(coords):
                self.results = None
                self.error_message.append("Coordinates are not always bidimensional.")

            case (
                (east1, north1),
                *_,
                (eastn, northn),
            ) if not self._validates_are_transformable_to_float(coords):
                self.results = None
                self.error_message.append(
                    "Coordinates are not all and transformable to float"
                )

            case _:
                self.results = None
                self.error_message.append("Invalid coords. Unknown error.")

    def _validates_boundaried_single_paired_coords(self, e, n):
        e_is_well_boundaried = e >= self.crs1._min_west and e < self.crs1._max_east
        n_is_well_boundaried = n >= self.crs1._min_south and n < self.crs1._max_north
        return e_is_well_boundaried and n_is_well_boundaried

    def _validates_are_transformable_to_float(self, *coords):
        for coord in coords:
            if self._validates_is_iterable(coord) and not isinstance(coord, str):
                if not self._validates_are_transformable_to_float(*coord):
                    return False
            else:
                if not self._is_transformable_to_float(coord):
                    return False
        return True

    def _transforms_single_coords_to_float(self, coords):
        return float(coords[0]), float(coords[1])

    def _validates_2d_float_sequence_boundaried_coordinates(self, coords):
        if self._validates_is_always_2d(coords):
            if self._validates_tuple_as_float_container(coords):
                return self._validates_boundaried_paired_coords(coords)
        return False

    def _2d_iterable_to_narray(self, coords):
        coords = np.array(coords).transpose()
        return coords[0], coords[1]

    def _validates_2d_float_transformable(self, coords):
        cond1 = self._validates_is_always_2d(coords)
        cond2 = self._validates_are_transformable_to_float(coords)
        return cond1 and cond2

    def _transforms_2d_tuple_to_float(self, coords):
        float_coords = []
        for coord in coords:
            float_coords.append((self._transforms_single_coords_to_float(coord)))
        return tuple(float_coords)

    def _validates_boundaried_paired_coords(self, coords):
        if self._validates_is_iterable(coords):
            coordinates = self._2d_iterable_to_narray(coords)
            return self._validates_are_boundaried(*coordinates)
        return False

    def _validates_are_boundaried(self, *coordinates):

        return (
            min(coordinates[0]) >= self.crs1._min_west
            and max(coordinates[0]) < self.crs1._max_east
        ) and (
            min(coordinates[1]) >= self.crs1._min_south
            and max(coordinates[1]) < self.crs1._max_north
        )

    def _validates_is_always_2d(self, coords):
        cond1 = self._validates_is_iterable(coords)
        cond2 = len(np.array(coords).shape) == 2
        cond3 = np.array(coords).shape[self.COL_ARRAY] == self.COORDS_2D
        return cond1 and cond2 and cond3

    def _validates_is_iterable(self, object):  # Here
        try:
            iter(object)
            return True
        except TypeError:
            return False

    def _validates_tuple_as_float_container(self, coords):
        return (
            np.array(coords).dtype == self.DTYPE_64
            or np.array(coords).dtype == self.DTYPE_32
        )

    def _is_transformable_to_float(self, coord):
        _is_transformable = False
        try:
            float(coord)
            _is_transformable = True
        except ValueError as e:
            print(f"Error: {e}")
        return _is_transformable


class EPSG21897_INTL1924_Projector(Projecter):

    CRSs = ("EPSG21897", "Hayford International 1924")
    STR_REPRESENTATION = "With %s and %s" % CRSs

    def __init__(self, crs1, crs2):
        super().__init__(crs1, crs2)
        print(self.STR_REPRESENTATION + " started")

    def __str__(self) -> str:
        return self.STR_REPRESENTATION

    def organizes_coordtype_pipeline(self, proj_to_geog: bool):
        return super().organizes_coordtype_pipeline(proj_to_geog)

    def _differentiates_input_patterns(self, coords, inverse):
        return super()._differentiates_input_patterns(coords, inverse)

    def projects_projected_to_geographic(self, coords):
        return super().projects_projected_to_geographic(coords)

    def projects_geographic_to_projected(self, coords):
        return super().projects_geographic_to_projected(coords)

    def get_results(self):
        return super().get_results()


if __name__ == "__main__":
    import doctest

    doctest.testfile("projections_tests.txt")

    # print("%.7f, %.7f" % wgs84)  # Adjust the format specifier accordingly
