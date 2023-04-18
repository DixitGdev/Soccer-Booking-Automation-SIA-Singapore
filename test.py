import time
from datetime import datetime
import pytz

SST = pytz.timezone('Asia/Singapore')

print(f"Date : {datetime.now(SST).date()}")
print(f"Current Time : {datetime.now(SST).hour}:{datetime.now(SST).minute}\n")
