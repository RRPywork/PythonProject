"""
Ложные тесты Автор - Балескин
"""
from Library.GUI.I_Data import MockDataAggregator

import unittest


class Test(unittest.TestCase):
    """Ложный пакет тестов Автор - Балескин"""
    def testDataInterface(self):
        """Ложный тест Автор - Балескин"""
        m = MockDataAggregator()
        self.assertEqual(m.get_data(), "SomeString Been in processing. Been in Aggregator.", "SmthHappened?")


if __name__ == "__main__":
    unittest.main()
