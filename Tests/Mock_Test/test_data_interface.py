"""
The world's fake
"""
import unittest

from Library.GUI.I_Data import MockDataAggregator

class TestDA(unittest.TestCase):
    """FAKEEEE"""
    def test_data_interface(self):
        """Liiies"""
        m_d_a = MockDataAggregator()
        self.assertEqual(m_d_a.get_data(), 1, "SmthHappened?")


if __name__ == "__main__":
    unittest.main()
