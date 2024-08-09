import os
from datetime import datetime

date_str = datetime.now().strftime('%Y-%m-%d')
file_path = os.path.join('Documentation', 'README.md')

entry = f"| {date_str} | | | | |\n"

with open(file_path, 'a') as f:
    f.write(entry)

print(f"Added daily update for {date_str}")
