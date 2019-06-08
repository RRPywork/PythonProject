"""
Описывает интерфейс, используемый для взаимодействия с DatabaseParser
Author: Daniil (Progger)
"""
from abc import ABC
from abc import abstractmethod


class DBInterface(ABC):
    """
    Абстрактный класс-интерфейс Автор  Балескин
    """
    @abstractmethod
    def parse(self, *pargs):
        """Абстрактный метод. Должен быть унаследован потомками. Парсит БД и возвращает данные"""


class MockDataParser(DBInterface):
    """
    Класс-наследник, парсер БД Автор - Балескин
    """
    def parse(self, *pargs):
        """Функция-Наследник"""
        return "SomeString"
        
    def __init__(self):
        """Конструктор - Автор Балескин"""
        pass
