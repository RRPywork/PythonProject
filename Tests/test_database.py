"""Автор: Балескин"""
import unittest

from Library.DataBase import DataBase
from Library.database_interaction.DatabaseParser import DatabaseParser


class Test(unittest.TestCase):
    """
    Класс для тестирования классов Database и DatabaseParser
    Автор: Балескин
    """

    def test_appending_objects(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        # print(db.get_db())
        assert True

    def test_append_attributes(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        # print(db.get_db().loc["Evergreen"])
        assert True

    def test_object_deletion(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.delete_objects(["Evergreen"])
        # print(db.get_db())
        assert True

    def test_attribute_deletion(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.delete_attribute("Evergreenness")
        # print(db.get_db())
        assert True

    def test_get_objects(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        a = db.get_objects(["Evergreen", "NotEvergreen"])
        # print(a.get_db())
        assert True

    def test_get_attribute(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
        a = db.get_attributes(["Evergreenness"])
        # print(a.get_db())
        assert True

    def test_get_part(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
        a = db.get_part(["Evergreen", "VeryEvergreen"], ["Name"])
        # print(a.get_db())
        assert True

    def test_exclusive(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
        a = db.get_objects_exclusive(["Evergreen", "NotEvergreen"])
        b = db.get_attributes_exclusive(["Evergreenness"])
        # print(a.get_db())
        # print(b.get_db())
        assert True

    def test_store(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
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
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
        a = db.get_part_exclusive(["Evergreen", "NotEvergreen"], ["Evergreenness"])
        # print(a.get_db())
        assert True

    def test_init_from_db(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
        a = DataBase(db.get_db())
        # print(a.get_db())

    def test_get_db(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
        # print(db.get_db())
        assert True

    def test_get_value(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
        # print(db.get_value("Evergreen", "Evergreenness") + 3)
        assert True

    def test_change_value(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
        # print(db.get_db())
        # print(db.change_value("Evergreen", "Evergreenness", 3))
        # print(db.get_db())
        assert True

    def test_rename(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
        db.rename({"Evergreen": "NotSoEvergreen"}, axis="index")
        db.rename({"Name": "NotSoLame"}, axis="columns")
        print(db.get_db())
        assert True

    def test_get_attr_names(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
        # print(db.get_attr_names());
        assert True

    def test_append_attributes_2(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
        db2 = DataBase()
        db2.append_object("Evergreen", ["Coolness", "Rank"], [10, 3])
        db2.append_object("NotEvergreen", ["Coolness", "Rank"], [1, 2])
        db2.append_object("VeryEvergreen", ["Coolness", "Rank"], [10, 1])
        db.append_attributes(["Coolness", "Rank"], db2)
        print(db.get_db())
        assert True

    def test_join(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
        db2 = DataBase()
        db2.append_object("Evergreen", ["Coolness", "Rank"], [10, 3])
        db2.append_object("NotEvergreen", ["Coolness", "Rank"], [1, 2])
        db2.append_object("VeryEvergreen", ["Coolness", "Rank"], [10, 1])
        db = db.join(db2, on=None, how="left")
        print(db.get_db())
        assert True

    def test_parser(self):
        """"""
        db = DataBase()
        db.append_object("Evergreen", ["Name"], ["Mary Sue"])
        db.append_object("NotEvergreen", ["Name"], ["Robert Katz"])
        db.append_attribute("Evergreenness", [1, 0])
        db.append_object("VeryEvergreen", ["Name", "Evergreenness"], ["Uncle Bob", 10])
        db2 = DataBase()
        db2.append_object("Evergreen", ["Coolness", "Rank"], [10, 3])
        db2.append_object("NotEvergreen", ["Coolness", "Rank"], [1, 2])
        db2.append_object("VeryEvergreen", ["Coolness", "Rank"], [10, 1])

        db3 = DataBase()
        db3.append_object("10", ["Rank_1"], [3])
        db3.append_object("1", ["Rank_1"], [2])
        print(db3.get_db())
        db.store("test_data")
        db2.store("test_data_2")
        db3.store("test_data_3")
        dp = DatabaseParser(["test_1", "test_2", "test_3"],
                            dict(zip(["test_1", "test_2", "test_3"], ["test_data", "test_data_2", "test_data_3"])),
                            hints={"test_1": "-", "test_2": "-", "test_3": "Coolness"})
        dp.parse("DISPLAY", ["-e", None], [None, None], None)
        print(dp.working_db.get_db())
        dp.parse("DISPLAY", ["-i", "Evergreenness", "Coolness"], ["-e", "VeryEvergreen"], None)
        print(dp.working_db.get_db())
        dp.parse("STORE", "test_total_1")
        dp.parse("DROP", ["test_1"])
        dp.parse("DISPLAY", ["-e", None], [None, None], None)
        print(dp.working_db.get_db())
        # dp.parse("DISPLAY", ["-e",None],[None,None],None)
        # print(dp.working_db.get_db())
        dp.parse("ADD", ["total_1"], ["test_total_1"], {"total_1": "-"})
        dp.parse("DISPLAY", ["-e", None], [None, None], None)
        print(dp.working_db.get_db())
        dp.parse("DELETE", ["Coolness_caller"], ["Evergreen"])
        print(dp.working_db.get_db())
        dp.parse("APPEND", ["Name"], ["EverNotGreen", "Everevergreeen"],
                 [{"Name": "Katz", "Rank": 3, "Evergreenness": 2, "Coolness_callee": 3},
                  {"Name": "Hui Yue", "Rank": 7, "Evergreenness": 1, "Coolness_callee": 5}], None)
        print(dp.working_db.get_db())
        dp.parse("CHANGE", "Name", "NotEvergreen", "Lin Yun")
        print(dp.working_db.get_db())
        dp.parse("RENAME", {"NotEvergreen": "NotSoEvergreen"}, "index")
        print(dp.working_db.get_db())
        dp.parse("RENAME", {"Name": "NotSoLame"}, "columns")
        print(dp.working_db.get_db())
        dp.parse("LOAD", "processors_v")
        print(dp.working_db.get_db())
        assert True


if __name__ == "__main__":
    unittest.main()
