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
        """
        Абстрактный метод. Должен быть унаследован потомками.
        Нужен, если, например, надо рассчитать (или обсчитать) какой-нибудь атрибут
        """

    #@abstractmethod
    def evaluate(self, obj_name)->bool:
        """
        :param obj_name: имя исследуемого объекта
        :return:результат исчисления
        """
        pass

class empty_processor(IDataProcessor):
    """
    Процессор для замещения пустого условия
    """
    def _process(self, *pargs):
        pass

    def evaluate(self, obj_name):
        return True

class MockDataProcessor(IDataProcessor):
    """
    Класс-наследник
    """
    def _process(self, *pargs):
        """Функция-Наследник"""
        return 1

    def __init__(self):
        pass
