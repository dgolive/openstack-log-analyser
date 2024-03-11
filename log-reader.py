import os
import re
from datetime import datetime
import pandas as pd

arr_errors = []
with open('logs/cinder-backup.log', 'r') as log_file:
    for line in log_file:
        if re.search('ERROR', line) and re.search('] ', line):
            arr_errors.append( line.split('] ')[-1].strip() )

pd.set_option('display.max_colwidth', None)
df = pd.DataFrame(arr_errors)
df.columns = ['mgs']
df = df.groupby(['mgs']).size().reset_index()
df.columns = ['mgs', 'count']
print(df)