""""""
import unittest

from Library.DataBase import DataBase


class Test(unittest.TestCase):
    """"""

    def test_appending_objects(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        # print(db.get_db())
        assert True

    def test_append_attributes(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        # print(db.get_db().loc["Evergreen"])
        assert True

    def test_object_deletion(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.delete_objects(["Evergreen"])
        # print(db.get_db())
        assert True

    def test_attribute_deletion(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.delete_attribute("Evergreenness")
        # print(db.get_db())
        assert True

    def test_get_objects(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        a = db.get_objects(["Evergreen", "NotEvergreen"])
        # print(a.get_db())
        assert True

    def test_get_attribute(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        a = db.get_attributes(["Evergreenness"])
        # print(a.get_db())
        assert True

    def test_get_part(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        a = db.get_part(["Evergreen", "VeryEvergreen"], ["Name"])
        # print(a.get_db())
        assert True

    def test_exclusive(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        a = db.get_objects_exclusive(["Evergreen", "NotEvergreen"])
        b = db.get_attributes_exclusive(["Evergreenness"])
        # print(a.get_db())
        # print(b.get_db())
        assert True

    def test_store(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        db.store("test_data")
        assert True

    def test_read(self):
        """"""
        db = DataBase()
        db.read("test_data")
        # print(db.get_db())
        assert True

    def test_get_part_exclusive(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        a = db.get_part_exclusive(["Evergreen", "NotEvergreen"], ["Evergreenness"])
        # print(a.get_db())
        assert True

    def test_init_from_db(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        a = DataBase(db.get_db())
        # print(a.get_db())

    def test_get_db(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        # print(db.get_db())
        assert True

    def test_get_value(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        print(db.get_value("Evergreen", "Evergreenness") + 3)
        assert True

    def test_change_value(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen",["Name"],["Mary Sue"])
        db.append_object("NotEvergreen",["Name"],["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob",  10])
        print(db.get_db())
        print(db.change_value("Evergreen", "Evergreenness", 3))
        print(db.get_db())
        assert True


if __name__ == "__main__":
    unittest.main()
