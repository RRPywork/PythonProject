"""
Попытка создать БД
"""


class DataBase:
    """
    Класс с БД - это лучший класс
    """
    def __init__(self):
        """"""
        self.DB = dict()

    def append_objects(self, objects):
        """"""
        assert self.DB.get(objects[0]) is None
        self.DB[objects[0]] = objects[1]

    def append_attributes(self, attr_name, attr_values):
        """"""
        for key in self.DB.keys():
            self.DB[key][attr_name] = attr_values[key]

    def delete_objects(self, object_keys):
        """"""
        for i in object_keys:
            assert self.DB.get(i) is not None
            self.DB.pop(i)

    def delete_attribute(self, attr_name):
        """"""
        for key in self.DB.keys():
            self.DB.get(key).pop(attr_name)

    def get_objects(self, keys):
        """"""
        k = {i: self.DB[i] for i in self.DB.keys() if i in keys}
        return k

    def get_attributes(self, attr_names):
        """"""
        k = dict()
        for j in self.DB.keys():
            k[j] = {i: self.DB.get(j).get(i) for i in attr_names}
        return k

    def get_part(self, keys, attr_names):
        """"""
        if attr_names is None:
            return self.get_objects(keys)
        if keys is None:
            return self.get_attributes(attr_names)
        k = {i: self.DB[i] for i in self.DB.keys() if i in keys}
        a = dict()
        for j in k.keys():
            a[j] = {i: k.get(j).get(i) for i in attr_names}
        return a
