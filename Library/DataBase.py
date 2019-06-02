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
    def __init__(self, db=None, name=None):
        """"""
        if db is None:
            self.db = DataFrame()
        else:
            self.db = DataFrame(db)
        if name is None:
            self.name = ''
        else:
            self.name = name

    def get_db(self):
        """"""
        return self.db

    def get_attr_names(self):
        d = [i for i in self.db.keys()]
        return d;

    def append_object(self, index, column_data, object_data):
        """"""
        self.db = self.db.append(Series(object_data, index=column_data, name=index))

    def append_attribute(self, attr_name, attr_values):
        """"""
        self.db[attr_name] = attr_values

    def append_attributes(self, attr_names, db):
        """"""
        for i in attr_names:
            self.append_attribute(i, db.get_attributes([i]).get_db())

    def delete_objects(self, object_keys):
        """"""
        self.db = self.db.drop(object_keys, axis=0)

    def delete_attribute(self, attr_name):
        """"""
        if attr_name is not None:
            self.db = self.db.drop([attr_name], axis=1)

    def get_value(self, key, attr_name):
        """"""
        return self.db.at[key, attr_name]

    def change_value(self, key, attr_name, new_value):
        """"""
        temp = self.get_value(key, attr_name)
        self.db[attr_name].loc[key] = new_value
        return temp

    def rename(self, mapper, axis):
        """"""
        self.db = self.db.rename(mapper, axis=axis)

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
        """"""
        k = self.db.drop(attr_names, axis=1)
        a = k.drop(keys, axis=0)
        return DataBase(a)

    def get_name(self):
        return self.name

    def join(self, other, on, how):
        """"""
        db = DataFrame(self.db)
        if self.db.empty:
            return DataBase(other.get_db(), name=self.name)
        return DataBase(db.join(other.get_db(), on, how, lsuffix="_caller", rsuffix="_callee"))

    def empty(self):
        """"""
        return self.db.empty

    def store(self, filename):
        """"""
        path = '..\\Data\\'
        self.db.to_csv(path + filename + '.csv', index=True)

    def read(self, filename):
        """"""
        path = '..\\Data\\'
        self.db = read_csv(path + filename + '.csv', index_col=0)
        print(self.db)
