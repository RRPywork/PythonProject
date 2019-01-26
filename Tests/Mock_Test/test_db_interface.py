"""
DCSTR
"""
import unittest

from Library.DataFlow.DBInterface import MockDataParser

class TestDBI(unittest.TestCase):
    """
    DCSTR
    """
    def test_data_base_interface(self):
        """DCSTR"""
        d_b_i = MockDataParser()
        self.assertEqual(d_b_i.parse(), 1, "something happened?")

if __name__ == "__main__":
    unittest.main()
