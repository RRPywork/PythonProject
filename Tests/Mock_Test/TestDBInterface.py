"""
The world's fake
"""
from Library.DataFlow.DBInterface import MockDataParser

import unittest

class test(unittest.TestCase):
    """FAKEEEE"""
    def testDataInterface(self):
        """Liiies"""
        m = MockDataParser()
        self.assertEqual(m.parse(), "SomeString", "SmthHappened?")


if __name__ == "__main__":
    unittest.main()

