# General outline:

# Read the list of log files in the "logs" folder
# For each log file
#       Read each line from the log
#       

# Print the accumulated flight time

import csv
import os

##############################################################################
################################  Constants  #################################
##############################################################################

LOGS_FOLDER_NAME = 'logs'

##############################################################################
#################################  Methods  ##################################
##############################################################################

def retrieveLogsList(folder_name):
    original_path = os.getcwd()

    if not isinstance(folder_name,str):
        raise TypeError('Please enter a valid folder name')
    
    # Change cwd to the logs folder
    os.chdir(os.path.join(os.getcwd(),folder_name))

    files = os.listdir(os.getcwd())
    logs_filenames = [os.path.join(os.getcwd(),f) for f in files
                      if f[-3:] == 'log']
    
    os.chdir(original_path)
    return logs_filenames

def computeFlightTime(log_filename):
    CURR_ROW_NAME = 'CURR'
    ROW_NAME_INDEX = 0
    CURRENT_THRESHOLD = 4

    V32_MULTIPLIERS = {'firmware_version': 'V3.2', 'current_multiplier': 1}    
    V33_MULTIPLIERS = {'firmware_version': 'V3.3', 'current_multiplier': 100}
    V34_MULTIPLIERS = {'firmware_version': 'V3.4', 'current_multiplier': 1}
    
    flight_time = 0

    if not isinstance(log_filename,str) or log_filename[-3:] != 'log':
        raise TypeError('Please enter a valid log filename.' +
                        ' Filename entered: "%s"' % (log_filename))

    print log_filename
    
    drone_flying = False
    last_takeoff = -1
    timeus_index = -1
    firmware_version = ''
    current_multiplier = 1
    time_multiplier = 1
    with open(log_filename,'rb') as log:
        log_reader = csv.reader(log)
        for row in log_reader:
            # Find headers
            if timeus_index == -1:
                timeus_index, curr_index = findIndexOfTimeAndCurrInRow(row)
            
            if row[ROW_NAME_INDEX] == CURR_ROW_NAME:

                if firmware_version.startswith(V33_MULTIPLIERS['firmware_version']):
                    current_multiplier = V33_MULTIPLIERS['current_multiplier']
                elif firmware_version.startswith(V34_MULTIPLIERS['firmware_version']):
                    current_multiplier = V34_MULTIPLIERS['current_multiplier']
                elif firmware_version.startswith(V32_MULTIPLIERS['firmware_version']):
                    current_multiplier = V32_MULTIPLIERS['current_multiplier']
                    time_multiplier = 1000
                
                row_timeus = time_multiplier*float(row[timeus_index].strip())
                row_current = float(row[curr_index].strip())

                if row_current >= current_multiplier*CURRENT_THRESHOLD:
                    if not drone_flying:
                        last_takeoff = row_timeus
                        drone_flying = True
                elif drone_flying:
                    flight_time += row_timeus - last_takeoff
                    drone_flying = False
            elif firmware_version == '':
                firmware_version = findFirmwareVersionInRow(row)
    
    return flight_time/1e6
    
def computeTotalFlightTime(logs_list):
    total_flight_time = 0

    if not isinstance(logs_list,list):
        raise TypeError('Please enter a list of log filenames')
    
    for log_filename in logs_list:
        total_flight_time += computeFlightTime(log_filename)
    
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

def findIndexOfTimeAndCurrInRow(row):
    TIMEUS_ENTRY_NAME = 'TIMEUS'
    CURR_ENTRY_NAME = 'CURR'

    timeus_index = -1
    curr_index = -1
    
    curr_header = findCurrHeaderInRow(row)
    if curr_header != []:
        #timeus_index = getEntryIndexFromHeader(curr_header,TIMEUS_ENTRY_NAME)
        timeus_index = 1
        curr_index = getEntryIndexFromHeader(curr_header,CURR_ENTRY_NAME)
    
    return timeus_index,curr_index

def findFirmwareVersionInRow(row):
    ROW_NAME_INDEX = 0
    MSG_ROW_NAME = 'MSG'
    FIRMWARE_ENTRY_INDEX = -1
    firmware_string = row[FIRMWARE_ENTRY_INDEX]

    if row[ROW_NAME_INDEX] == MSG_ROW_NAME:
        start_firmware = firmware_string.find('V') # Assuming always starts with V
        end_firmware = firmware_string.find(' ',start_firmware)
        end_firmware = end_firmware if end_firmware != -1 else len(firmware_string)
        return firmware_string[start_firmware:end_firmware]
    return ''

if __name__ == '__main__':
    folder_name = LOGS_FOLDER_NAME
    logs_list = retrieveLogsList(folder_name)
    print 'Analysing %s logs...' % (len(logs_list))
    #print 'Flight time: %s' % (computeFlightTime(logs_list[86]))
    total_flight_time = computeTotalFlightTime(logs_list)
    print 'Total flight time: %s s' % (total_flight_time)
