# main.py
'''
WebScrape HOPS Staging Server
Process ID Viewer

'''

import pandas as pd
from sys import exit
from io import StringIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from threading import Event
from time import strftime
from os import remove, system, path, mkdir
from auth import my_user, my_path, hops_pass, dummy, dummy_staging
from variables import HOPS_Staging_dict, HOPS_dict, TOC, id_list


def main_function():
    system('cls')  # Clear the Console for ease of viewing
    today = strftime("%Y_%m_%d-%H_%M_%S")  # Gives initial a date time stamp
    the_day = strftime('%Y_%m_%d')  # Give a date stamp
    no_id_found = []
    no_acks_left = []

    # Setup Chrome Browser
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=options)  # Put your webdriver into PATH
    # I like smaller windows, ** Don't make it too small though
    driver.set_window_size(600, 700)

    # Allows the Choice of TOC to be controlled outside the code
    for x in TOC:
        print(x)
        # 2 Create the Staging url path here from the dict
        y = HOPS_Staging_dict[x]
        dumb_url = 'https://' + y + dummy_staging
        driver.get(dumb_url)

        # 2 Create the Live url path here from the dict
        # y = HOPS_dict[x]
        # dumb_url = 'https://' + y + dummy
        # driver.get(dumb_url)

        # Use Authorisation module
        driver.find_element_by_name("username").send_keys(my_user)
        driver.find_element_by_name("password").send_keys(hops_pass)
        driver.find_element_by_name("submit").click()
        Event().wait(2)

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
                print(f'There is no "Search Result" for Proess ID {process_x}')
                no_id_found.append(process_x)
            Event().wait(2)

            # Pull the table from the page
            dumbtable = str(y + today + 'dumbtable.csv')

            # Catch exception when there are no Pending ACKs
            try:
                tagged = driver.find_element_by_id('missingAcks').text
                s = StringIO(tagged)

                # Write file Locally
                with open(dumbtable, 'w') as f:
                    for item in s:
                        f.write(item)

                # 7 Create datestamped folders
                dir = path.join(my_path, the_day)
                if not path.exists(dir):
                    mkdir(dir)

            # 5 Manipulate the dataframe
                df = pd.DataFrame(pd.read_csv(dumbtable))
                df = df.iloc[1:]  # Removed the busted header row
                # Splits the text into three columns
                df = df.iloc[:, 0].str.split(expand=True)
                df.columns = ["ISAM ID", "Frame Source", "Frame FTS"]

            # 6 Create date time stamped file
                file_label = str(dir) + '/HOPS_' + \
                    x + '_' + process_x + '_' + today + '.csv'
                df.to_csv(file_label, index=False, header=True)
                remove(dumbtable)  # Removes Local file
                print(f'Pending ACKs for {process_x} have been saved to {dir}')
                # Update the time stamp to prevent overwrite
                today = strftime("%Y_%m_%d-%H_%M_%S")
            except NoSuchElementException:
                print(
                    f'There are no "Pending ACKs" for Process ID {process_x}')
                no_acks_left.append(process_x)
                # Update the time stamp to prevent overwrite
                today = strftime("%Y_%m_%d-%H_%M_%S")

        dir = path.join(my_path, the_day)
        if not path.exists(dir):
            mkdir(dir)

        no_acks_left_filename = path.join(
            dir, ('ProcessIDs with No Pending Acks ' + x + ' ' + today + '.txt'))
        with open(no_acks_left_filename, 'w') as f:
            f.write(str(no_acks_left))

        no_searchs_filename = path.join(
            dir, ('ProcessIDs Not Found for ' + x + ' ' + today + '.txt'))
        with open(no_searchs_filename, 'w') as f:
            f.write(str(no_id_found))

    driver.quit()


if __name__ == "__main__":
    main_function()
