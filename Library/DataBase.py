"""
Попытка создать БД
"""

from pandas import DataFrame
from pandas import Series
from pandas import read_csv


class DataBase:
    """
    Класс с БД - это лучший класс
    """
    def __init__(self):
        """"""
        self.db = DataFrame()

    def append_object(self, index, column_data, object_data):
        """"""
        self.db = self.db.append(Series(object_data, index=column_data, name=index))

    def append_attribute(self, attr_name, attr_values):
        """"""
        self.db[attr_name] = attr_values

    def delete_objects(self, object_keys):
        """"""
        self.db = self.db.drop(object_keys, axis=0)

    def delete_attribute(self, attr_name):
        """"""
        self.db = self.db.drop([attr_name], axis=1)

    def get_objects(self, keys):
        """"""
        k = self.db.loc[keys, :]
        return k

    def get_objects_exclusive(self, keys):
        """"""
        k = self.db.drop(keys, axis=0)
        return k

    def get_attributes(self, attr_names):
        """"""
        k = self.db[attr_names]
        return k

    def get_attributes_exclusive(self, attr_names):
        """"""
        k = self.db.drop(attr_names, axis=1)
        return k

    def get_part(self, keys, attr_names):
        """"""
        if attr_names is None:
            return self.get_objects(keys)
        if keys is None:
            return self.get_attributes(attr_names)
        k = self.db[attr_names].loc[keys,:]
        return k

    def get_part_exclusive(self, keys, attr_names):
        k = self.db.drop(attr_names, axis=1)
        a = k.drop(keys, axis=0)
        return a

    def store(self, filename):
        """"""
        path = '..\\Data\\'
        self.db.to_csv(path + filename + '.csv', index=True)

    def read(self, filename):
        """"""
        path = '..\\Data\\'
        self.db = read_csv(path + filename + '.csv', index_col=0)
