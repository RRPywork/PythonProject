"""
The world's fake
"""
from Library.GUI.I_Data import MockDataAggregator

import unittest


class Test(unittest.TestCase):
    """FAKEEEE"""
    def testDataInterface(self):
        """Liiies"""
        m = MockDataAggregator()
        self.assertEqual(m.get_data(), "SomeString Been in processing. Been in Aggregator.", "SmthHappened?")


if __name__ == "__main__":
    unittest.main()
