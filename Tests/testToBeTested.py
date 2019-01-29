"""
DOCSTR
"""

from Scripts.file import to_be_tested

import unittest


class Tests(unittest.TestCase):
    """
    dcstr
    """
    def testTBT(self):
        self.assertEqual(to_be_tested(), 3)

    def testTBTFail(self):
        self.assertEqual(to_be_tested(), 4, "Testing toBeTested failed")


if __name__ == "__main__":
    unittest.main()
