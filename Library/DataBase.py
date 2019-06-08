"""
БД
Автор: Балескин
"""
import os
from pandas import DataFrame
from pandas import Series
from pandas import read_csv


class DataBase:
    """
    Автор: Балескин
    Содержит pandas.DataFrame и замещает его, с целью инкапсуляции лишнего функционала там, где он не нужен
    """

    def __init__(self, db=None, name=None):
        """Конструктор от DataFrame и имени БД Автор - Балескин"""
        if db is None:
            self.db = DataFrame()
        else:
            self.db = DataFrame(db)
        if name is None:
            self.name = ''
        else:
            self.name = name

    def get_db(self):
        """Позволяет получить подлежащий DataFrame Автор - Балескин"""
        return self.db

    def get_attr_names(self):
        """Позволяет получить список атрибутов БД. Автор - Балескин"""
        d = [i for i in self.db.keys()]
        return d

    def append_object(self, index, column_data, object_data):
        """Позволяет добавить объект. Автор - Балескин. Вход - данные об объекте"""
        self.db = self.db.append(Series(object_data, index=column_data, name=index))

    def append_attribute(self, attr_name, attr_values):
        """Позволяет добавить атрибут. Автор - Балескин. Вход - данные об атрибуте"""
        self.db[attr_name] = attr_values

    def append_attributes(self, attr_names, db):
        """Позволяет добавить множество атрибутов. Автор - Балескин. Вход - данные об атрибутах"""
        for i in attr_names:
            self.append_attribute(i, db.get_attributes([i]).get_db())

    def delete_objects(self, object_keys):
        """Позволяет удалить объекты. Автор - Балескин. Вход - ключи объектов"""
        self.db = self.db.drop(object_keys, axis=0)

    def delete_attribute(self, attr_name):
        """Позволяет удалить атрибут. Автор - Балескин. Вход - имя атрибута"""
        if attr_name is not None:
            self.db = self.db.drop([attr_name], axis=1)

    def get_value(self, key, attr_name):
        """Позволяет получить значение ячейки. Автор Балескин. Вход - ключ объекта и имя атрибута"""
        return self.db.at[key, attr_name]

    def change_value(self, key, attr_name, new_value):
        """Позволяет изменить значение ячейки. Автор Балескин. Вход - ключ объекта и имя атрибута, новое значение
        возвращает старое значение"""
        temp = self.get_value(key, attr_name)
        self.db[attr_name].loc[key] = new_value
        return temp

    def rename(self, mapper, axis):
        """Позволяет переименовать объект или атрибут Автор - Балескин"""
        self.db = self.db.rename(mapper, axis=axis)

    def get_objects(self, keys):
        """Позволяет получить множество объектов по их ключам Автор - Балескин"""
        k = self.db.loc[keys, :]
        return DataBase(k)

    def get_objects_exclusive(self, keys):
        """Позволяет получить все объекты кроме данных. Задаются объекты в виде ключей Автор - Балескин"""
        k = self.db.drop(keys, axis=0)
        return DataBase(k)

    def get_attributes(self, attr_names):
        """Позволяет получить множество атрибутов по их ключам Автор - Балескин"""
        k = self.db[attr_names]
        return DataBase(k)

    def get_attributes_exclusive(self, attr_names):
        """Позволяет получить все атрибуты кроме данных. Задаются атрибуты по их названиям Автор - Балескин"""
        k = self.db.drop(attr_names, axis=1)
        return DataBase(k)

    def get_part(self, keys, attr_names):
        """Позволяет получить подмножество БД по указанным ключам объектов и именам атрибутов Автор - Балескин"""
        if attr_names is None:
            return self.get_objects(keys)
        if keys is None:
            return self.get_attributes(attr_names)
        k = self.db[attr_names].loc[keys, :]
        return DataBase(k)

    def get_part_exclusive(self, keys, attr_names):
        """Позволяет получить подмножество БД по ключам объектов и именам атрибутов, исключая указанные Автор - Балескин"""
        k = self.db.drop(attr_names, axis=1)
        a = k.drop(keys, axis=0)
        return DataBase(a)

    def get_name(self):
        """Позволяет получить имя БД Автор - Балескин"""
        return self.name

    def join(self, other, on, how):
        """Позволяет слить две БД Автор - Балескин"""
        db = DataFrame(self.db)
        if self.db.empty:
            return DataBase(other.get_db(), name=self.name)
        return DataBase(db.join(other.get_db(), on, how, lsuffix="_caller", rsuffix="_callee"))

    def empty(self):
        """Позволяет проверить, не пуста ли БД Автор - Балескин"""
        return self.db.empty

    def store(self, filename):
        """Позволяет сохранить БД в файл Автор - Балескин"""
        path = os.path.dirname(os.path.realpath(__file__)) + '\\..\\Data\\'
        self.db.to_csv(path + filename + '.csv', index=True)

    def read(self, filename):
        """Позвоялет считать БД из файла"""
        from pathlib import Path
        path = os.path.dirname(os.path.realpath(__file__)) + '\\..\\Data\\'
        path += filename + '.csv'
        file = Path(path)
        if not file.is_file():
            raise RuntimeError("Not a file")
        self.db = read_csv(path, index_col=0)

        # print(self.db)
