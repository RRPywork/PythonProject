""""""
class Block:
    """"""
    def __init__(self, block_name):
        """"""
        self.name = block_name
        self.items = dict()

    def add_item(self, item_name, item_value):
        self.items[item_name]=item_value



class ConfigurationParser:
    """"""
    def __init__(self, path):
        """"""
        self.path = path
        self.blocks = dict()

    def parse(self):
        """"""
        with open(self.path, 'r') as f:
            block_name = ""
            strs=f.readlines()
            for line in strs:
                if line[0]=='[':
                    block_name = line[1:-2]
                    self.blocks[block_name]=Block(block_name)
                elif line!="":
                    name, val = line.split('=')
                    val = val[:-1] if val[-1]=='\n' else val
                    self.blocks[block_name].add_item(name, val)
        return self.blocks
