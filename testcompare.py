#!/bin/env python
import compare
import unittest

class CompareTest(unittest.TestCase):
    def testcompare(self):
	result = compare.compare(5,3)
	self.assertEquals(result, True)

if __name__ == "__main__":
    unittest.main()








