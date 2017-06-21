# General outline:

# Read the list of log files in the "logs" folder
# For each log file
#       Read each line from the log
#       

# Print the accumulated flight time

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
    logs_filenames = [f for f in files if f[-3:] == 'log']
    
    os.chdir(original_path)
    return logs_filenames

def computeFlightTime(log_filename):
    return 0
    
def computeTotalFlightTime(logs_list):
    total_flight_time = 0

    if not isinstance(logs_list,list):
        raise TypeError('Please enter a list of log filenames')
    
    for log_filename in logs_list:
        total_flight_time += computeFlightTime(log_filename)
    
    return total_flight_time
    
if __name__ == '__main__':
    folder_name = LOGS_FOLDER_NAME
    logs_list = retrieveLogsList(folder_name)
    print 'Analysing %s logs...' % (len(logs_list))
    total_flight_time = computeTotalFlightTime(logs_list)
    print 'Total flight time: %s s' % (total_flight_time)
