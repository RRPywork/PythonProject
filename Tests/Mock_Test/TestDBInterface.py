"""
Ложные тесты Автор-Балескин
"""
from Library.DataFlow.DBInterface import MockDataParser

import unittest


class Test(unittest.TestCase):
    """Класс ложных тестов Автор-Балескин"""
    def test_data_interface(self):
        """Ложный тест Автор - Балескин"""
        m = MockDataParser()
        self.assertEqual(m.parse(), "SomeString", "SmthHappened?")


if __name__ == "__main__":
    unittest.main()

