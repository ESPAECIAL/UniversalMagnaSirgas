from abc import ABC, abstractclassmethod

class MagnaSirgasCRS(ABC):
    @abstractclassmethod
    def crs(self):
        pass
    @abstractclassmethod
    def max_north(self):
        pass
    @abstractclassmethod
    def min_south(self):
        pass
    @abstractclassmethod
    def max_east(self):
        pass
    @abstractclassmethod
    def min_west(self):
        pass
    def __repr__(self) -> str:
        return f"MagnaSirgasCRS()"