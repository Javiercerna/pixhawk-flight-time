import unittest
import os
import random
import sys

from flight_time import retrieveLogsList, createLogObject, \
             computeFlightTime, computeTotalFlightTime, \
             formatSeconds

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

    def test_createLogObject(self):
        # Test 1: Handle bad input (no string)
        self.assertRaises(TypeError,createLogObject,42)
        self.assertRaises(TypeError,createLogObject,[])
        # Test 2: Handle bad input (no log files)
        self.assertRaises(TypeError,createLogObject,
                          '104 5-12-2016 2-15-40 p. m..bin')
        self.assertRaises(TypeError,createLogObject,
                          '2016-10-28 12-34-41.px4')
        # Test 3: Check for blank filename
        self.assertRaises(TypeError,createLogObject,'')
        # Test 4: Check known logs
        log_names = ['2017-05-09 09-41-26.log',
                     '200 11-04-2017 3-20-00 p. m..bin.log',
                     '2017-03-31 11-06-44.log',
                     '2016-11-09 16-33-24.log']
        expected_firmware = ['V3.4','V3.4','V3.3','V3.2']
        for ind in range(len(log_names)):
            filename = os.path.join(os.getcwd(),LOGS_FOLDER_NAME,log_names[ind])
            log_object = createLogObject(filename)
            self.assertEqual(log_object['firmware_version'],expected_firmware[ind],
                            'Firmware version doesnt match expected')
        
    def test_computeFlightTime(self):
        # Test 1: Handle bad input (no dictionary)
        self.assertRaises(TypeError,computeFlightTime,42)
        self.assertRaises(TypeError,computeFlightTime,[])
        self.assertRaises(TypeError,computeFlightTime,'firmware_version')
        # Test 2: Handle bad input (incomplete objects)
        log_object = {'firmware_version': 'V3.2'}
        self.assertRaises(TypeError,computeFlightTime,log_object)
        log_object = {'timeus_entries' : [], 'current_entries' : []}
        self.assertRaises(TypeError,computeFlightTime,log_object)
        # Test 3: Check known logs
        log1 = '2017-05-09 09-41-26.log'
        expected_flight_time = 2.5*60
        filename = os.path.join(os.getcwd(),LOGS_FOLDER_NAME,log1)
        flight_time = computeFlightTime(createLogObject(filename))
        time_error = abs(expected_flight_time - flight_time)
        self.assertTrue(time_error < 0.1*expected_flight_time,
                        'Flight time doesnt match expected')
        log2 = '200 11-04-2017 3-20-00 p. m..bin.log'
        expected_flight_time = 0
        filename = os.path.join(os.getcwd(),LOGS_FOLDER_NAME,log2)
        flight_time = computeFlightTime(createLogObject(filename))
        time_error = abs(expected_flight_time - flight_time)
        self.assertTrue(time_error < (expected_flight_time+1),
                         'Flight time doesnt match expected')
        log3 = '2017-03-31 11-06-44.log'
        expected_flight_time = 19*60
        filename = os.path.join(os.getcwd(),LOGS_FOLDER_NAME,log3)
        flight_time = computeFlightTime(createLogObject(filename))
        time_error = abs(expected_flight_time - flight_time)
        self.assertTrue(time_error < 0.1*expected_flight_time,
                        'Flight time doesnt match expected')
        log4 = '2016-11-09 16-33-24.log'
        expected_flight_time = 0
        filename = os.path.join(os.getcwd(),LOGS_FOLDER_NAME,log4)
        flight_time = computeFlightTime(createLogObject(filename))
        time_error = abs(expected_flight_time - flight_time)
        self.assertTrue(time_error < (expected_flight_time+1),
                         'Flight time doesnt match expected')
    
    def test_computeTotalFlightTime(self):
        # Test 1: Handle bad input (no list)
        self.assertRaises(TypeError,computeTotalFlightTime,42)
        self.assertRaises(TypeError,computeTotalFlightTime,'')
        # Test 2: Check that no logs give a flight time of 0.
        total_flight_time = computeTotalFlightTime([])
        self.assertEqual(total_flight_time,0,
                         'The total flight time is not 0 for []')

    def test_formatSeconds(self):
        # Test 1: Handle bad input (no float)
        self.assertRaises(TypeError,formatSeconds,'42')
        self.assertRaises(TypeError,formatSeconds,[42])
        # Test 2: Handle bad input (negative seconds)
        self.assertRaises(ValueError,formatSeconds,-10)
        # Test 3: Check known cases
        expected_times = ['00:00:00','00:00:30','00:01:00','00:10:30',
                          '01:00:00','02:00:30','03:20:30']
        seconds_to_test = [0,30,60,630,3600,7230,12030]
        for ind in range(len(expected_times)):
            formatted_time = formatSeconds(seconds_to_test[ind])
            self.assertEqual(formatted_time,expected_times[ind],
                             'Time formatted doesnt match expected')
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
