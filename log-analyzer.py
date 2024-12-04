import os
import re
from datetime import datetime

import re
import pandas as pd

# log_directory = 'logs' # Replace with the correct Logs folder path

# target_date_time = datetime(2023, 10, 20, 12, 00, 00)  # Replace with your desired date and time

print("")
print("Log Analyser")
log_directory = input("Log Folder Path: ")
print("Enter with year, month, day, hour, minutes and seconds. The logs will gather from this date onwards")
input_date_time = input("sample format: 2023, 10, 30, 12, 00, 00: ")
input_date_time_split = input_date_time.split(', ')
print(input_date_time)
target_date_time = datetime(int(input_date_time_split[0]), int(input_date_time_split[1]), int(input_date_time_split[3]), int(input_date_time_split[4]), int(input_date_time_split[5]))
print(target_date_time)

error_patterns = [
    r'ERROR',  # Add more error patterns as needed
    r'Exception',
    r'failed',
]

arr_errors = []
for root, dirs, files in os.walk(log_directory):
    for file in files:
        if file.endswith('.log'):
            log_file_path = os.path.join(root, file)
            with open(log_file_path, 'r') as log_file:
                for line_number, line in enumerate(log_file, start=1):
                    log_timestamp = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
                    if log_timestamp:
                        log_timestamp = datetime.strptime(log_timestamp.group(), '%Y-%m-%d %H:%M:%S')
                        if log_timestamp >= target_date_time:
                            if any(re.search(pattern, line) for pattern in error_patterns):
                                # print(f'Error message found in: {log_file_path} (Line {line_number}): {line}') 
                                # print(line) 
                                # for l in line:
                                arr_errors.append(line.split(']')[-1]) #struct is the same and get the last part
                                # arr_errors.append( l.split('] ')[-1].strip() )
# print(arr_errors[0])

pd.set_option('display.max_colwidth', None)
df = pd.DataFrame(arr_errors)
print(df)
df.columns = ['mgs']
df = df.groupby(['mgs']).size().reset_index()
df.columns = ['mgs', 'count']
print(df)