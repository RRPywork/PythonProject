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
    def get_data(self, *pargs):
        """Абстрактный метод. Должен быть унаследован потомками. Возвращает обработанные данные"""

    @abstractmethod
    def _process(self, *pargs):
        """Производит обработку данных по запросу"""

    @abstractmethod
    def _get_raw_data(self):
        """Добывает необработанные данные."""


class MockDataAggregator(DataInterface):
    """Класс-наследник, агрегатор данных"""
    def get_data(self, *pargs):
        """Функция-Наследник"""
        data = self._process()
        return data

    def _process(self, *pargs):
        """См. интерфейс"""
        data = self._get_raw_data()
        return data

    def _get_raw_data(self):
        """см. интерфейс"""
        return 1

    def __init__(self):
        pass
