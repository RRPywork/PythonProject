"""
Описывает интерфейс, используемый для взаимодействия с DataFlow
Author: Vitaly (Admin)
"""
from abc import ABC
from abc import abstractmethod

class DataInterface(ABC):
    """
    Абстрактный класс-интерфейс
    """
    @abstractmethod
    def getData(self, *pargs):
        """Абстрактный метод. Должен быть унаследован потомками. Возвращает обработанные данные"""
        pass

    @abstractmethod
    def _process(self, *pargs):
        """Производит обработку данных по запросу"""
        pass


    def _getRawData(self):
        """Добывает необработанные данные."""
        pass


class MockDataAggregator(DataInterface):
    """Класс-наследник, агрегатор данных"""
    def getData(self, *pargs):
        """Функция-Наследник"""
        Data = self._process()
        if Data == 1:
            return 1
        else:
            return 0

    def _process(self, *pargs):
        """См. интерфейс"""
        Data = self._getRawData()
        if Data == 1:
            return 1
        else:
            return 0

    def _getRawData(self):
        """см. интерфейс"""
        return 1

    def __init__(self):
        pass
