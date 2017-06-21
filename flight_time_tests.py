import unittest
import os, sys

from flight_time import retrieveLogsList, computeTotalFlightTime

class FlightTimeTest(unittest.TestCase):

    def test_retrieveLogsList(self):
        # Test 1: Handle bad input (no string)
        self.assertRaises(TypeError,fun=retrieveLogsList,folder_name=42)
        self.assertRaises(TypeError,fun=retrieveLogsList,folder_name=[])
        # Test 2: Check that multiple runs give the same result
        result = retrieveLogsList('logs')
        for dummy_ind in range(100):
            self.assertEqual(retrieveLogsList('logs'),result)
    
    def test_computeTotalFlightTime(self):
        # Test 1: Handle bad input (no list)
        self.assertRaises(TypeError,fun=computeTotalFlightTime,
                          logs_list=42)
        self.assertRaises(TypeError,fun=computeTotalFlightTime,
                          logs_list='')
        # Test 2: Check that no logs give a flight time of 0.
        total_flight_time = computeTotalFlightTime([])
        self.assertEqual(total_flight_time,0)
        
        
if __name__ == '__main__':
    unittest.main()
