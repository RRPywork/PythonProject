"""
The world's fake
"""
from Library.GUI.I_Data import MockDataAggregator

import unittest

class test(unittest.TestCase):
    """FAKEEEE"""
    def testDataInterface(self):
        """Liiies"""
        M =MockDataAggregator()
        self.assertEqual(M.getData(), 1, "SmthHappened?")


if __name__ == "__main__":
    unittest.main()
