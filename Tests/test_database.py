""""""
import unittest

from Library.DataBase import DataBase


class Test(unittest.TestCase):
    """"""

    def test_appending_objects(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        # print(db.db)
        assert True

    def test_append_attributes(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        # print(db.db.loc["Evergreen"])
        assert True

    def test_object_deletion(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.delete_objects(["Evergreen"])
        # print(db.db)
        assert True

    def test_attribute_deletion(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.delete_attribute("Evergreenness")
        # print(db.db)
        assert True

    def test_get_objects(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        a = db.get_objects(["Evergreen", "NotEvergreen"])
        # print(a)
        assert True

    def test_get_attribute(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        a = db.get_attributes(["Evergreenness"])
        # print(a)
        assert True

    def test_get_part(self):
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        a = db.get_part(["Evergreen", "VeryEvergreen"], ["Name"])
        # print(a)
        assert True

    def test_exclusive(self):
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        a = db.get_objects_exclusive(["Evergreen", "NotEvergreen"])
        b = db.get_attributes_exclusive(["Evergreenness"])
        # print(a)
        # print(b)
        assert True

    def test_store(self):
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        db.store("test_data")
        assert True

    def test_read(self):
        db = DataBase()
        db.read("test_data")
        # print(db.db)
        assert True

    def test_get_part_exclusive(self):
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        a = db.get_part_exclusive(["Evergreen", "NotEvergreen"], ["Evergreenness"])
        print(a)
        assert True

if __name__ == "__main__":
    unittest.main()
