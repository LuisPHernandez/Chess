import unittest
import sys
import os

sys.path.append(os.path.expanduser('~/Documents/Dev/Chess/src/code'))

from chess_ai import *

# Creating a test case
class TestAddNumbers(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(add_numbers(2, 3), 5)  # Test case 1
        self.assertEqual(add_numbers(-1, 1), 0) # Test case 2
        self.assertEqual(add_numbers(0, 0), 0)  # Test case 3

# Running the tests
if __name__ == '__main__':
    unittest.main()