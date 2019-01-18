"""
DOCSTR
"""

from Scripts.file import toBeTested

import unittest

class tests(unittest.TestCase):

    def testTBT(self):
        self.assertEqual(toBeTested(), 3)

    def testTBTFail(self):
        self.assertEqual(toBeTested(), 4, "Testing toBeTested failed")


if __name__ == "__main__":
    unittest.main()
