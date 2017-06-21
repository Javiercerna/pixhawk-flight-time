import unittest
import os, sys

from flight_time import retrieveLogsList

class FlightTimeTest(unittest.TestCase):

    def test_retrieveLogsList(self):
        # Test 1: Handle bad input (no string)
        self.assertRaises(TypeError,fun=retrieveLogsList,folder_name=42)
        self.assertRaises(TypeError,fun=retrieveLogsList,folder_name=[])
        # Test 2: Check that multiple runs give the same result
        result = retrieveLogsList('logs')
        for dummy_ind in range(100):
            self.assertEqual(retrieveLogsList('logs'),result)
            
if __name__ == '__main__':
    unittest.main()
