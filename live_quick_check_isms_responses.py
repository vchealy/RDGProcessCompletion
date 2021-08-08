# live_quick_check.py
'''
    WebScrape HOPS Server
    Process ID Viewer

	Opens the process viewer for specific process ID. (Taken from a variables module)
	Confirming that the process is on the server and that ISMS auth has completed.
'''

import winsound
from sys import exit
from io import StringIO

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from threading import Event
from time import strftime
from os import system, path, mkdir
from auth import my_user, my_path, hops_pass, dummy
from variables import HOPS_dict, id_Live_dict, TOC

def main_function():
    # Allows the Choice of TOC to be controlled outside the code
    for x in TOC:
        controller(x)
    print('Task Complete.')
    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)


def controller(x):
    system('cls')  # Clear the Console for ease of viewing
    today = strftime("%Y_%m_%d-%H_%M_%S")  # Gives an initial date time stamp
    the_day = strftime('%Y_%m_%d')  # Gives a date stamp
    no_id_found = []
    no_isms_left = []
    pending_acks_there = []

    # Setup Chrome Browser
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=options)  # Put your webdriver into PATH
    driver.set_window_size(600, 700)  # I like smaller windows, ** Don't make it too small though

    print(f'Live - {x}')
    # Create the Live url path here from the HOPS_dict
    y = HOPS_dict[x]
    dumb_url = 'https://' + y + dummy
    driver.get(dumb_url)

    # Use Authorisation module
    driver.find_element_by_name("username").send_keys(my_user)
    driver.find_element_by_name("password").send_keys(hops_pass)
    driver.find_element_by_name("submit").click()
    Event().wait(2)

    # Select the correct TOC List of Process IDs
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
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            no_id_found.append(process_x)
        Event().wait(2)
        pending_acks_there.append(process_x)

        # Catch exception when there are no ISMS Responses
        try:
            tagged = driver.find_element_by_id('responses').text

            # Create datestamped folders
            dir = path.join(my_path, the_day)
            if not path.exists(dir):
                mkdir(dir)
            print(f'There are "ISMS Responses" for Process ID {process_x}')
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

        except NoSuchElementException:
            no_isms_left.append(process_x)
            continue
        # # Create Folder
        # dir = path.join(my_path, the_day)
        # if not path.exists(dir):
        #     mkdir(dir)

        # # For no Process ID
        # if len(no_id_found) > 0:  # Where All 'Process ID are not found' file created
        #     no_searchs_filename = path.join(
        #         dir, ('ProcessIDs Not Found for ' + x + ' ' + today + '.txt'))
        #     with open(no_searchs_filename, 'w') as f:
        #         f.write(str(no_id_found))

        # # Ensures no_id_found is not on no_isms_left list
        # no_isms_left = list(set(no_isms_left) - set(no_id_found))

        # if len(no_isms_left) > 0:  # Where all 'ProcessIDs have No ISMS Responses' file created
        #     no_isms_left_filename = path.join(
        #         dir, ('ProcessIDs with ISMS Responses ' + x + ' ' + today + '.txt'))
        #     with open(no_isms_left_filename, 'w') as f:
        #         f.write(str(no_isms_left))

        # if len(pending_acks_there) > 0:  # Where all 'ProcessIDs have ISMS Responses' file created
        #     pending_acks_there_filename = path.join(
        #         dir, ('ProcessIDs with ISMS Responses ' + x + ' ' + today + '.txt'))
        #     with open(pending_acks_there_filename, 'w') as f:
        #         f.write(str(pending_acks_there))

    driver.quit()
    return


if __name__ == "__main__":
    main_function()
