"""
Описывает интерфейс, используемый для взаимодействия с DatabaseParser
Author: Daniil (Progger)
"""
from abc import ABC
from abc import abstractmethod

class DBInterface(ABC):
    """
    Абстрактный класс-интерфейс
    """
    @abstractmethod
    def parse(self, *pargs):
        """Абстрактный метод. Должен быть унаследован потомками. Парсит БД и возвращает данные"""
        pass

class MockDataParser(DBInterface):
    """
    Класс-наследник, парсер БД
    """
    def parse(self, *pargs):
        """Функция-Наследник"""
        return 1
        
    def __init__(self):
        pass
    