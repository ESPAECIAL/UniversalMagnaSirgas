import logging

import numpy as np

from crs import MagnaSirgasCRS
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.DEBUG)


class SimpleAdapter(ABC):

    # The column index in an array
    COL_ARRAY = 1
    # floats for a projected coordinate in two dimensions
    COORDS_2D = 2
    # Numpy type for the 64 bytes float
    DTYPE_64 = np.dtype(np.float64).type
    # Numpy type for the 32 bytes float
    DTYPE_32 = np.dtype(np.float32).type
    NAME = "SimpleAdapter"
    PROJECTION = "forward-projection"
    INVERSE_PROJECTION = "inverse-projection"
    ELIP_TRANSFORMATION = "elipsoidal-transformation"

    @abstractmethod
    def _validates_coord_types(self, crs1, crs2):
        return True if self._are_crs_magnasirgascrs_subclasses(crs1, crs2) else False

    def get_results(self):
        return self.results

    def _log_origin_target_arenot_projectable(self, crs1, crs2):
        return logging.error(
            f"The crs' {crs1, crs2} do not create a pipeline to project because they're not Magna Sirgas CRS"
        )

    def _differentiates_input_patterns(self, coords, functional="forward-projection"):
        self._matches_single_2d_coords(coords, functional=functional)
        if not self._coords_are_single_paired:
            self._matches_not_single_2d_coords(coords, functional=functional)
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

    def _matches_single_2d_coords(self, coords, functional="transformation"):
        self._coords_are_single_paired = True
        match coords:
            case (
                float(east),
                float(north),
            ) if self._validates_boundaried_single_paired_coords(east, north):
                self._segmentates_functionals(east, north, functional=functional)

            case (
                float(east),
                float(north),
            ) if not self._validates_boundaried_single_paired_coords(east, north):
                self.Warning_message.append(
                    "Coordinates are not all within the crs boundaries."
                )
                self._segmentates_functionals(east, north, functional=functional)

            case (east, north) if self._validates_are_transformable_to_float(
                east, north
            ):
                float_e, float_n = self._transforms_single_coords_to_float(coords)
                self.warning_message.append("Coordinates were transform to floats.")
                if not self._validates_boundaried_single_paired_coords(east, north):
                    self.warning_message.append(
                        "Coordinates are not all within the crs boundaries."
                    )
                self._segmentates_functionals(float_e, float_n, functional=functional)

            case (east, north) if not self._validates_are_transformable_to_float(
                east, north
            ):
                self.error_message.append(
                    "Coordinates can not be transformed to floats."
                )
                self.results = None
            case _:
                self._coords_are_single_paired = False

    def _matches_not_single_2d_coords(self, coords, functional="transformation"):
        match coords:

            case (
                (east1, north1),
                *_,
                (eastn, northn),
            ) if self._validates_2d_float_sequence_boundaried_coordinates(coords):
                narrays_coords = self._2d_iterable_to_narray(coords)
                self._segmentates_functionals(*narrays_coords, functional=functional)

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
                self._segmentates_functionals(*narrays_coords, functional=functional)

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

    def _segmentates_functionals(self, *coords, functional="transformation"):
        if functional == self.PROJECTION:
            self.results = self.projection(*coords, inverse=False)
        elif functional == self.INVERSE_PROJECTION:
            self.results = self.projection(*coords, inverse=True)
        elif functional == self.ELIP_TRANSFORMATION:
            self.results = self.transformation(*coords)
        elif functional == self.INVERSE_ELIP_TRANSFORMATION:
            print("A")

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

    def __repr__(self) -> str:
        return f"{self.NAME}({self.crs1}, {self.crs2})"

    def __str__(self) -> str:
        return f"{self.NAME}"

    def exchanges_crs(self):
        temp = self.crs1
        self.crs1 = self.crs2
        self.crs2 = temp

    def _is_magnasirgascrs_subclass(self, crs):
        return isinstance(crs, MagnaSirgasCRS)

    def _are_crs_magnasirgascrs_subclasses(self, *many_crs):
        for crs in many_crs:
            if not self._is_magnasirgascrs_subclass(crs):
                return False
        return True

    def _which_are_not_magnasirgascrs_subclasses(self, *manycrs):
        not_magnasirgas_crs = list()
        for crs in manycrs:
            if not self._is_magnasirgascrs_subclass(crs):
                not_magnasirgas_crs.append(crs)
        return tuple(not_magnasirgas_crs)

    def _origin_target_arenot_magnasirgascrs_log(self, crs1, crs2):
        not_magna_sirgas_crs = self._which_are_not_magnasirgascrs_subclasses(crs1, crs2)
        logging.error(f"{not_magna_sirgas_crs} are not subclasses of {MagnaSirgasCRS}")
        raise KeyError(f"{not_magna_sirgas_crs} are not subclasses of {MagnaSirgasCRS}")
