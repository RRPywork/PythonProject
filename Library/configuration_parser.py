"""Автор: Балескин"""
import os


class Block:
    """
    Хранит один блок файла ini
    Автор: Балескин
    """

    def __init__(self, block_name):
        """Конструктор от имени блока Автор-Балескин"""
        self.name = block_name
        self.items = dict()

    def add_item(self, item_name, item_value):
        """Добавление элемента Автор - Балескин"""
        self.items[item_name] = item_value


class ConfigurationParser:
    """Обработчик файла конфигурации Автор: Балескин"""

    def __init__(self, path):
        """Конструктор от пути к файлу Автор-Балескин"""
        self.path = path
        self.blocks = dict()

    def parse(self):
        """Обработка. Возвращает элементы файла Автор Балескин"""
        # print(os.path.dirname(os.path.realpath(__file__)))
        with open(os.path.dirname(os.path.realpath(__file__)) + '\\..\\Scripts\\' + self.path, 'r') as f:
            block_name = ""
            strs = f.readlines()
            for line in strs:
                if line[0] == '[':
                    block_name = line[1:-2]
                    self.blocks[block_name] = Block(block_name)
                elif line != "":
                    name, val = line.split('=')
                    val = val[:-1] if val[-1] == '\n' else val
                    self.blocks[block_name].add_item(name, val)
        return self.blocks
