"""
Содержит обработчик запросов к базе данных.
Задача: искоренить влияние Pandas (по возможности) из потока данных. Поток данных не должен от него зависеть.
Вполне возможно (и так действительно может получиться!), обработчики и GUI будут частично зависеть от Pandas,
(используем Pandas как обертку для MatPlotLib) но потоку не должно быть никакого дела до передаваемых по нему объектов.
Author: Vitaly(Admin)
"""
from Library.DataBase import DataBase
from Library.DataFlow.DBInterface import DBInterface


class DatabaseParser(DBInterface):
    """
    Обработчик
    """
    def __init__(self, names, paths):
        """
        Конструктор. Добывает БД из файлов csv (или sql, или ... Смотря что в методе)
        и помещает их в словарь отношение:БД
        """
        assert len(names) == len(paths)
        self.its_dbs = {i:DataBase() for i in names}
        for i in names:
            self.its_dbs[i].read(paths[i])

    def parse(self, *pargs):
        """
        Метод, отвечающий за обработку.
        Выполняет выбор типа операции в зависимости от аргументов (в частности, первого) и делегирует частным случаям.
        """
        pass
