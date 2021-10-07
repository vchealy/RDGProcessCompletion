import schedule
import time
from sys import exit
'''
    Schedule the running of the main code
    All TOCs can take over an hour for IOKE scrape to complete
'''
# import in the function/s I want to schedule
# from live_quick_check import main_function as qmf
from live_isam_and_frame_count import main_function as mf

# Choose the selection - For the purpose of the blog I will use just this
# schedule.every().day.at("11:00").do(qmf)
schedule.every().day.at("07:00").do(mf)
# schedule.every().day.at("13:00").do(mf)
# schedule.every().day.at("16:30").do(mf)
# schedule.every(5).minutes.do(mf)

while True:
    schedule.run_pending()
    time.sleep(1)
else:
    exit()
