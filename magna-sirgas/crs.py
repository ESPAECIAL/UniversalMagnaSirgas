from abc import ABC, abstractmethod, abstractclassmethod, property

class MagnaSirgasCRS(ABC):
    @abstractclassmethod
    def type(cls):
        pass
    @classmethod
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
    @abstractclassmethod
    def crs(self):
        pass
    def __repr__(self) -> str:
        return f"MagnaSirgasCRS()"