import schedule
import time
from sys import exit
'''
    Schedule the quick check
    This repeats the QuickCheck code that is looking to see if the ISMS auth has completed
'''
# import in the function/s I want to schedule
from live_quick_check import main_function as qmf 

# Choose the timer - First run will start after the initial timer has ran
# Look to set another schedule if you need it to run it initially.
schedule.every(15).minutes.do(qmf)

while True:
    schedule.run_pending()
    time.sleep(1)
else:
    exit()