from abc import ABC, abstractmethod


class MagnaSirgasCRS(ABC):
    @abstractmethod
    def crs(self):
        pass

    @abstractmethod
    def max_north(self):
        pass

    @abstractmethod
    def min_south(self):
        pass

    @abstractmethod
    def max_east(self):
        pass

    @abstractmethod
    def min_west(self):
        pass

    def __repr__(self) -> str:
        return f"MagnaSirgasCRS()"
