import os
import re
from datetime import datetime

log_directory = '/var/log/kolla' # Replace with the correct Openstack Logs folder path

target_date_time = datetime(2023, 10, 30, 12, 00, 00)  # Replace with your desired date and time

error_patterns = [
    r'ERROR',  # Add more error patterns as needed
    r'Exception',
    r'failed',
]

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
                                print(f'Error message found in: {log_file_path} (Line {line_number}): {line}')