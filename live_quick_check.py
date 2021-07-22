# live_quick_check.py
'''
    WebScrape HOPS Staging Server
    Process ID Viewer

	Open the process viewer for specific process ID. (Taken from a variables module)
	
	Confirming if an ISAM has picked up and successfully processed the message in the Process ID 
    or whether further action is required. 
	 - Unsuccessful is when there is a Pending ACK remaining for an ISAM for the above Process ID 
	
	**main.py**  
	    Automation of the TOC Process ID checks from the Process ID information supplied 
'''

import pandas as pd
from sys import exit
from io import StringIO

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

from threading import Event
from time import strftime
from os import remove, system, path, mkdir
from auth import my_user, my_path, hops_pass, dummy, dummy_staging
from variables import HOPS_Staging_dict, HOPS_dict, id_Live_dict, TOC


def main_function():
    system('cls')  # Clear the Console for ease of viewing
    today = strftime("%Y_%m_%d-%H_%M_%S")  # Gives initial a date time stamp
    the_day = strftime('%Y_%m_%d')  # Give a date stamp
    no_id_found = []
    no_acks_left = []
    pending_acks_there = []

    # Setup Chrome Browser
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=options)  # Put your webdriver into PATH
    # I like smaller windows, ** Don't make it too small though
    driver.set_window_size(600, 700)

    # Allows the Choice of TOC to be controlled outside the code
    for x in TOC:
        print(f'Live - {x}')
        # 2 Create the Live url path here from the dict
        y = HOPS_dict[x]
        dumb_url = 'https://' + y + dummy
        driver.get(dumb_url)

        # Use Authorisation module
        driver.find_element_by_name("username").send_keys(my_user)
        driver.find_element_by_name("password").send_keys(hops_pass)
        driver.find_element_by_name("submit").click()
        Event().wait(2)

        # Select the correct List of Process IDs
        id_list = list(id_Live_dict[x])
        print(id_list)

        # Process ID List Loop Starts Here
        for process_x in id_list:
            # Enter AMS > Process Viewer in the search box
            driver.find_element_by_link_text("AMS").click()
            driver.find_element_by_link_text("Process Viewer").click()
            Event().wait(2)
            driver.find_element_by_id(
                "ProcessSearch_processInstanceId").click()
            driver.find_element_by_id(
                "ProcessSearch_processInstanceId").clear()
            driver.find_element_by_id(
                "ProcessSearch_processInstanceId").send_keys(process_x)
            driver.find_element_by_id("ProcessSearch_search").click()
            Event().wait(2)

            # Catch when the Process ID is not on that HOPS
            try:
                driver.find_element_by_link_text("Detail").click()
            except NoSuchElementException:
                print(
                    f'There is no "Search Result" for Process ID {process_x}')
                no_id_found.append(process_x)
            Event().wait(2)
            pending_acks_there.append(process_x)

            # Page 1
            # Catch exception when there are no Pending ACKs
            try:
                tagged = driver.find_element_by_id('missingAcks').text

                # 7 Create datestamped folders
                dir = path.join(my_path, the_day)
                if not path.exists(dir):
                    mkdir(dir)

            except NoSuchElementException:
                print(
                    f'There are no "Pending ACKs" for Process ID {process_x}')
                no_acks_left.append(process_x)
                continue
            # Create Folder if there were no Process IDs or ACKs still pending
            dir = path.join(my_path, the_day)
            if not path.exists(dir):
                mkdir(dir)

            # For no Process ID
            if len(no_id_found) > 0:  # Where All 'Process ID are not found' file created
                no_searchs_filename = path.join(
                    dir, ('ProcessIDs Not Found for ' + x + ' ' + today + '.txt'))
                with open(no_searchs_filename, 'w') as f:
                    f.write(str(no_id_found))

            # Ensures no_id_found is not on no_acks_left list
            no_acks_left = list(set(no_acks_left) - set(no_id_found))

            if len(no_acks_left) > 0:  # Where all 'ProcessIDs have No Pending ACKs' file created
                no_acks_left_filename = path.join(
                    dir, ('ProcessIDs with No Pending Acks ' + x + ' ' + today + '.txt'))
                with open(no_acks_left_filename, 'w') as f:
                    f.write(str(no_acks_left))

            if len(pending_acks_there) > 0:  # Where all 'ProcessIDs have No Pending ACKs' file created
                pending_acks_there_filename = path.join(
                    dir, ('ProcessIDs with Pending Acks ' + x + ' ' + today + '.txt'))
                with open(pending_acks_there_filename, 'w') as f:
                    f.write(str(pending_acks_there))

    driver.quit()


if __name__ == "__main__":
    main_function()
