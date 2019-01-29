"""
Создает фабрику различных обработчиков БД
Author: Vitaly (Admin)
"""

from Library.DataFlow.DBInterface import MockDataParser

class DataParserFactory:
    """
    Фабрика
    """
    @staticmethod
    def create_mock_data_parser():
        """
        test method
        """
        return MockDataParser()
