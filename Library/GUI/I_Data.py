"""
Описывает интерфейс, используемый для взаимодействия с DataFlow
Author: Vitaly (Admin)
"""
from abc import ABC
from abc import abstractmethod

from Library.DataFlow.DBFactory import DataParserFactory

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
        return data + " Been in Aggregator."

    def _process(self, *pargs):
        """См. интерфейс"""
        Data = self._get_raw_data()
        return Data + " Been in processing."

    def _get_raw_data(self):
        """см. интерфейс"""
        return self.its_parser.parse()

    def __init__(self):
        self.its_parser = DataParserFactory.create_mock_data_parser()
