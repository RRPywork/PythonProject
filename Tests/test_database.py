""""""
import unittest

from Library.DataBase import DataBase


class Test(unittest.TestCase):
    """"""

    def test_appending_objects(self):
        """"""
        db = DataBase()
        db.append_objects(["Evergreen", {"Name": "Mary Sue"}])
        self.assertEqual(db.DB, {"Evergreen": {"Name": "Mary Sue"}}, "Wrong!")

    def test_append_attributes(self):
        """"""
        db = DataBase()
        db.append_objects(["Evergreen", {"Name": "Mary Sue"}])
        db.append_objects(["NotEvergreen", {"Name": "Robert Katz"}])
        db.append_attributes("Evergreenness", {"Evergreen": 1, "NotEvergreen": 0})
        self.assertEqual(db.DB["Evergreen"]["Evergreenness"], 1)
        self.assertEqual(db.DB["NotEvergreen"]["Evergreenness"], 0)

    def test_object_deletion(self):
        """"""
        db = DataBase()
        db.append_objects(["Evergreen", {"Name": "Mary Sue"}])
        db.append_objects(["NotEvergreen", {"Name": "Robert Katz"}])
        db.delete_objects(["Evergreen"])
        self.assertEqual(db.DB.get("Evergreen"), None)
        self.assertNotEqual(db.DB.get("NotEvergreen"), None)

    def test_attribute_deletion(self):
        """"""
        db = DataBase()
        db.append_objects(["Evergreen", {"Name": "Mary Sue", "Evergreenness": 1}])
        db.append_objects(["NotEvergreen", {"Name": "Robert Katz", "Evergreenness": 0}])
        db.delete_attribute("Evergreenness")
        self.assertEqual(db.DB.get("Evergreen").get("Evergreenness"), None)
        self.assertEqual(db.DB.get("NotEvergreen").get("Evergreenness"), None)

    def test_get_objects(self):
        """"""
        db = DataBase()
        db.append_objects(["Evergreen", {"Name": "Mary Sue", "Evergreenness": 1}])
        db.append_objects(["NotEvergreen", {"Name": "Robert Katz", "Evergreenness": 0}])
        db.append_objects(["VeryEvergreen", {"Name": "Uncle Bob", "Evergreenness": 10}])
        a = db.get_objects(["Evergreen", "VeryEvergreen"])
        self.assertEqual(a, {"Evergreen": {"Name": "Mary Sue", "Evergreenness": 1},
                             "VeryEvergreen": {"Name": "Uncle Bob", "Evergreenness": 10}})

    def test_get_attributes(self):
        """"""
        db = DataBase()
        db.append_objects(["Evergreen", {"Name": "Mary Sue", "Evergreenness": 1, "Params": 0}])
        db.append_objects(["NotEvergreen", {"Name": "Robert Katz", "Evergreenness": 0, "Params": 1}])
        db.append_objects(["VeryEvergreen", {"Name": "Uncle Bob", "Evergreenness": 10, "Params": 2}])
        a = db.get_attributes(["Name", "Params"])
        self.assertEqual(a, {"Evergreen": {"Name": "Mary Sue", "Params": 0},
                             "NotEvergreen": {"Name": "Robert Katz", "Params": 1},
                             "VeryEvergreen": {"Name": "Uncle Bob", "Params": 2}})

    def test_get_part(self):
        db = DataBase()
        db.append_objects(["Evergreen", {"Name": "Mary Sue", "Evergreenness": 1, "Params": 0}])
        db.append_objects(["NotEvergreen", {"Name": "Robert Katz", "Evergreenness": 0, "Params": 1}])
        db.append_objects(["VeryEvergreen", {"Name": "Uncle Bob", "Evergreenness": 10, "Params": 2}])
        a = db.get_part(["Evergreen", "VeryEvergreen"], ["Name", "Params"])
        self.assertEqual(a, {"Evergreen": {"Name": "Mary Sue", "Params": 0},
                             "VeryEvergreen": {"Name": "Uncle Bob", "Params": 2}})


if __name__ == "__main__":
    unittest.main()
