"""
DataFlow
Author: alesha
""" 
from abc import ABC 
from abc import abstractmethod 


class IDataProcessor(ABC):
    """
    Абстрактный класс-интерфейс
    """
    @abstractmethod
    def _process(self, *pargs):
        """Абстрактный метод. Должен быть унаследован потомками. """


class MockDataProcessor(IDataProcessor):
    """
    Класс-наследник
    """
    def _process(self, *pargs):
        """Функция-Наследник"""
        return 1

    def __init__(self):
        pass
