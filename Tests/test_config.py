"""Тесты файлов конфигурации Автор - Балескин"""
import unittest

from Library.configuration_parser import ConfigurationParser


class Test(unittest.TestCase):
    """Тест оббработчика конфигурации Автор - Балескин"""

    def test_config(self):
        """Тестирующая функция Автор - Балескин"""
        cp = ConfigurationParser("..\\Scripts\\config.ini")
        blocks = cp.parse()
        for name, b in blocks.items():
            print(name, ":\n")
            for pname, pval in b.items.items():
                print(pname, " = ", pval, "\n")
        assert True


if __name__ == "__main__":
    unittest.main()
