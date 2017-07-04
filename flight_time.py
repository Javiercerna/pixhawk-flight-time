import argparse
import csv
import os

##############################################################################
################################  Constants  #################################
##############################################################################

LOGS_FOLDER_NAME = 'logs'
LOG_FILE_EXTENSION = '.log'

##############################################################################
#################################  Methods  ##################################
##############################################################################

def retrieveLogsList(folder_name):
    '''
    Saves the logs filenames in a list. Uses the absolute path name to
    avoid storing the folder name as a separate parameter.
    '''
    original_path = os.getcwd()
    
    # Validate input
    if not isinstance(folder_name,str):
        raise TypeError('Please enter a valid folder name')
    
    # Change cwd to the logs folder
    os.chdir(os.path.join(os.getcwd(),folder_name))

    files = os.listdir(os.getcwd())
    logs_filenames = [os.path.join(os.getcwd(),f) for f in files
                      if f.endswith(LOG_FILE_EXTENSION)]
    
    os.chdir(original_path)
    return logs_filenames

def createLogObject(log_filename):
    '''
    Creates a log object with the desired properties as key value pairs.
    
    This method is needed since sometimes CURR measurements appear before
    the firmware version is shown and the multipliers cannot be computed.
    '''
    CURR_ROW_NAME = 'CURR'
    ROW_NAME_INDEX = 0
    TIMEUS_INDEX = 1

    # Validate input
    if not isinstance(log_filename,str) or not(log_filename.endswith(LOG_FILE_EXTENSION)):
        raise TypeError('Please enter a valid log filename.' +
                        ' Filename entered: "%s"' % (log_filename))
    
    # Initialize empty log object
    log_object = {'firmware_version' : '',
                        'curr_index' : -1,
                    'timeus_entries' : [],
                   'current_entries' : []}
    
    # Store desired properties in log_object
    with open(log_filename,'rb') as log:
        log_reader = csv.reader(log)
        for row in log_reader:
            if log_object['firmware_version'] == '':
                log_object['firmware_version'] = findFirmwareVersionInRow(row)
            if log_object['curr_index'] == -1:
                log_object['curr_index'] = findCurrIndexInRow(row)
            if row[ROW_NAME_INDEX] == CURR_ROW_NAME:
                curr_index = log_object['curr_index']
                log_object['timeus_entries'].append(float(row[TIMEUS_INDEX].strip()))
                log_object['current_entries'].append(float(row[curr_index].strip()))
    
    return log_object

def computeFlightTime(log_object):
    CURRENT_THRESHOLD = 4
    CURRENT_MULTIPLIERS = {'V3.2': 1, 'V3.3': 1.0/100, 'V3.4': 1, 'V3.7': 1}
    TIME_MULTIPLIERS = {'V3.2': 1000, 'V3.3': 1, 'V3.4': 1, 'V3.7': 1}

    # Validate input
    log_object_valid = 'firmware_version' in log_object and \
                       'curr_index' in log_object and \
                       'timeus_entries' in log_object and \
                       'current_entries' in log_object
    
    if not isinstance(log_object,dict) or not log_object_valid:
        raise TypeError('Please enter a valid log object.' +
                        ' Object entered: %s' % (log_object))
    
    current_multiplier = CURRENT_MULTIPLIERS[log_object['firmware_version']]
    time_multiplier = TIME_MULTIPLIERS[log_object['firmware_version']]
    
    drone_flying = False
    last_takeoff = -1
    flight_time = 0
    for entry_ind in range(len(log_object['timeus_entries'])):
        timeus = time_multiplier*log_object['timeus_entries'][entry_ind]
        current = current_multiplier*log_object['current_entries'][entry_ind]
        
        if current > CURRENT_THRESHOLD:
            if not drone_flying:
                last_takeoff = timeus
                drone_flying = True
        elif drone_flying:
            flight_time += timeus - last_takeoff
            drone_flying = False
    
    return flight_time/1e6
                
def computeTotalFlightTime(logs_list):
    total_flight_time = 0

    if not isinstance(logs_list,list):
        raise TypeError('Please enter a list of log filenames')
    
    for log_filename in logs_list:
        log_object = createLogObject(log_filename)
        total_flight_time += computeFlightTime(log_object)
    
    return total_flight_time

##############################################################################
############################  Helper functions  ##############################
##############################################################################

def getEntryIndexFromHeader(header,entry_name):
    entry_index = -1
    try:
        # Index starts at 1 (0 is header name)
        entry_index = header.index(entry_name) + 1
    except ValueError:
        print 'Entry "%s" not found in header: %s' % (entry_name,header)
    return entry_index

def findHeaderInRow(row,header_row_name):
    FMT_ROW_NAME = 'FMT'
    HEADER_FIRST_INDEX = 5
    
    if (row[0].strip() == FMT_ROW_NAME and row[3].strip() == header_row_name):
        curr_header = [header_element.strip().upper() for header_element
                       in row[HEADER_FIRST_INDEX:]]
        return curr_header
    return []

def findCurrHeaderInRow(row):
    return findHeaderInRow(row,'CURR')

def findCurrIndexInRow(row):
    CURR_ENTRY_NAME = 'CURR'
    
    curr_index = -1
    
    curr_header = findCurrHeaderInRow(row)
    if curr_header != []:
        curr_index = getEntryIndexFromHeader(curr_header,CURR_ENTRY_NAME)
    
    return curr_index

def findFirmwareVersionInRow(row):
    ROW_NAME_INDEX = 0
    MSG_ROW_NAME = 'MSG'
    FIRMWARE_ENTRY_INDEX = -1
    FIRMWARE_LENGTH = 4 # To save only V3.2, V3.3, V3.4
    firmware_string = row[FIRMWARE_ENTRY_INDEX]
    
    if row[ROW_NAME_INDEX] == MSG_ROW_NAME:
        start_firmware = firmware_string.find('V') # Assuming always starts with V
        return firmware_string[start_firmware:start_firmware+FIRMWARE_LENGTH]
    return ''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--log',help='single log filename')
    args = parser.parse_args()

    if args.log:
        flight_time = computeTotalFlightTime([args.log])
        print 'Flight time: %s s' % (flight_time)
    else:
        folder_name = LOGS_FOLDER_NAME
        logs_list = retrieveLogsList(folder_name)
        print 'Analyzing %s logs...' % (len(logs_list))
        total_flight_time = computeTotalFlightTime(logs_list)
        print 'Total flight time: %s s' % (total_flight_time)
