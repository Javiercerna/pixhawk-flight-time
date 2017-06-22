import unittest
import os
import random
import sys

from flight_time import retrieveLogsList, computeFlightTime, \
             computeTotalFlightTime

LOGS_FOLDER_NAME = 'logs'

class FlightTimeTest(unittest.TestCase):

    def test_retrieveLogsList(self):
        # Test 1: Handle bad input (no string)
        self.assertRaises(TypeError,retrieveLogsList,42)
        self.assertRaises(TypeError,retrieveLogsList,[])
        # Test 2: Check that multiple runs give the same result
        result = retrieveLogsList(LOGS_FOLDER_NAME)
        for dummy_ind in range(100):
            self.assertEqual(retrieveLogsList(LOGS_FOLDER_NAME),result,
                             'The logs list size has changed between runs')
        # Test 3: Check that the filenames retrieved exist
        result = retrieveLogsList(LOGS_FOLDER_NAME)
        for dummy_ind in range(100):
            random_log = random.choice(result)
            self.assertTrue(os.path.isfile(random_log),
                            'The log filename doesnt exist')

    def test_computeFlightTime(self):
        # Test 1: Handle bad input (no string)
        self.assertRaises(TypeError,computeFlightTime,42)
        self.assertRaises(TypeError,computeFlightTime,[])
        # Test 2: Handle bad input (no log files)
        self.assertRaises(TypeError,computeFlightTime,
                          '104 5-12-2016 2-15-40 p. m..bin')
        self.assertRaises(TypeError,computeFlightTime,
                          '2016-10-28 12-34-41.px4')
        # Test 3: Check for blank filename
        self.assertRaises(TypeError,computeFlightTime,'')
        # Test 4: Check known logs
        log1 = '2017-05-09 09-41-26.log'
        expected_flight_time = 2.5*60
        filename = os.path.join(os.getcwd(),LOGS_FOLDER_NAME,log1)
        flight_time = computeFlightTime(filename)
        time_error = abs(expected_flight_time - flight_time)
        self.assertTrue(time_error < 0.1*expected_flight_time,
                        'Flight time doesnt match expected')
        log2 = '200 11-04-2017 3-20-00 p. m..bin.log'
        expected_flight_time = 0
        filename = os.path.join(os.getcwd(),LOGS_FOLDER_NAME,log2)
        flight_time = computeFlightTime(filename)
        time_error = abs(expected_flight_time - flight_time)
        self.assertTrue(time_error < (expected_flight_time+1),
                         'Flight time doesnt match expected')
        log3 = '2017-03-31 11-06-44.log'
        expected_flight_time = 19*60
        filename = os.path.join(os.getcwd(),LOGS_FOLDER_NAME,log3)
        flight_time = computeFlightTime(filename)
        time_error = abs(expected_flight_time - flight_time)
        self.assertTrue(time_error < 0.1*expected_flight_time,
                        'Flight time doesnt match expected')
        # log4 = '2016-11-09 16-33-24.log'
        
        
    def test_computeTotalFlightTime(self):
        # Test 1: Handle bad input (no list)
        self.assertRaises(TypeError,computeTotalFlightTime,42)
        self.assertRaises(TypeError,computeTotalFlightTime,'')
        # Test 2: Check that no logs give a flight time of 0.
        total_flight_time = computeTotalFlightTime([])
        self.assertEqual(total_flight_time,0,
                         'The total flight time is not 0 for []')
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
