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
    def __init__(self, db=None):
        """"""
        if db is None:
            self.db = DataFrame()
        else:
            self.db = DataFrame(db)

    def get_db(self):
        """"""
        return self.db

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

    def get_value(self, key, attr_name):
        """"""
        return self.db.at[key, attr_name]

    def change_value(self, key, attr_name, new_value):
        """"""
        temp = self.get_value(key, attr_name)
        self.db[attr_name].loc[key] = new_value
        return temp

    def get_objects(self, keys):
        """"""
        k = self.db.loc[keys, :]
        return DataBase(k)

    def get_objects_exclusive(self, keys):
        """"""
        k = self.db.drop(keys, axis=0)
        return DataBase(k)

    def get_attributes(self, attr_names):
        """"""
        k = self.db[attr_names]
        return DataBase(k)

    def get_attributes_exclusive(self, attr_names):
        """"""
        k = self.db.drop(attr_names, axis=1)
        return DataBase(k)

    def get_part(self, keys, attr_names):
        """"""
        if attr_names is None:
            return self.get_objects(keys)
        if keys is None:
            return self.get_attributes(attr_names)
        k = self.db[attr_names].loc[keys,:]
        return DataBase(k)

    def get_part_exclusive(self, keys, attr_names):
        k = self.db.drop(attr_names, axis=1)
        a = k.drop(keys, axis=0)
        return DataBase(a)

    def store(self, filename):
        """"""
        path = '..\\Data\\'
        self.db.to_csv(path + filename + '.csv', index=True)

    def read(self, filename):
        """"""
        path = '..\\Data\\'
        self.db = read_csv(path + filename + '.csv', index_col=0)
