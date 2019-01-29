"""
The world's fake
"""
from Library.DataFlow.DBInterface import MockDataParser

import unittest


class Test(unittest.TestCase):
    """FAKEEEE"""
    def test_data_interface(self):
        """Liiies"""
        m = MockDataParser()
        self.assertEqual(m.parse(), "SomeString", "SmthHappened?")


if __name__ == "__main__":
    unittest.main()

