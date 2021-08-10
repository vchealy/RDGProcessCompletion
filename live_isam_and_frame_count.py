# live_isam_and_frame_count.py
''' 
    WebScrape HOPS Staging Server
    Process ID Viewer

	Open the process viewer for specific process ID. (Taken from a variables module)
    This code is to pull the full list of Pending ACKs for a Process ID.

    Multiple Process ID can be added for each TOC
    The output is a single XLSX file per TOC, on which there is a single sheet per Process ID

    Edit the variable.py file as required 

    *** Adjust the df to show a count of the total frames, unique ISAM numbers
'''
import pandas as pd
from io import StringIO

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from threading import Event
from time import strftime
from os import system, path, mkdir
from auth import my_user, my_path, hops_pass, dummy
from variables import TOC, HOPS_dict, id_Live_dict

def main_function():
    # This For loop is broken out, as XLSX writer was not completing for multiple TOCs
    for x in TOC:
        controller(x)
    print('Task Complete.')


def controller(x):
    system('cls')  # Clear the Console for ease of viewing
    today = strftime("%Y_%m_%d-%H_%M_%S")  # Gives an initial date time stamp
    the_day = strftime('%Y_%m_%d')  # Give a date stamp
    no_id_found = []
    pending_acks = []
    # Setup Chrome Browser
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=options)  # Put your webdriver into PATH
    driver.set_window_size(600, 700) # I like smaller windows, ** Don't make it too small though
    print(f'Live - {x}')

    # Create the Live url path here from the variables.py HOPS_dict
    y = HOPS_dict[x]
    dumb_url = 'https://' + y + dummy
    driver.get(dumb_url)

    # Use Authorisation module
    driver.find_element_by_name("username").send_keys(my_user)
    driver.find_element_by_name("password").send_keys(hops_pass)
    driver.find_element_by_name("submit").click()
    Event().wait(2)

    # Create datestamped folder
    dir = path.join(my_path, the_day)
    if not path.exists(dir):
        mkdir(dir)

    # Create a XLSX workbook per TOC
    name_file = str(dir + '/' + x + '_' + today +'.xlsx')
    writer = pd.ExcelWriter(name_file, engine='xlsxwriter')

    # Loop through the Process IDs
    # Choose the TOC Process ID list from variables.py > id_Live_dict
    process_id_list = list(id_Live_dict[x])
    print(process_id_list)

    # Get the complete table of Info for a Process ID
    for process_x in process_id_list:
        print(process_x) # Console view to understand which  Process Id is being worked on
        try:
            #Get to the specific page
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
            driver.find_element_by_link_text("Detail").click()

            # Catch when the Process ID is not on that HOPS
            try:
                driver.find_element_by_link_text("Detail").click()
            except NoSuchElementException:
                no_id_found.append(process_x)

            Event().wait(2)
            pending_acks.append(process_x)
            
            tagged = driver.find_element_by_id('missingAcks').text
            s = StringIO(tagged)
            df = pd.read_table(s, header= None)
            # Loop over each page for the Process ID
            next_page_btn = driver.find_element_by_xpath(("//*[text()='Next']"))
            while next_page_btn is not True:
                driver.find_element_by_xpath(("//*[text()='Next']")).click()
                # Pull the table from the page
                today = strftime("%Y_%m_%d-%H_%M_%S")  # Gives initial a date time stamp

                tagged = driver.find_element_by_id('missingAcks').text
                s = StringIO(tagged)
                df2 = pd.read_table(s, header= None)
                df = df.append(df2)
            else:
                print("No pages") # In case there isn't a table for that Process ID
                continue
        except NoSuchElementException:
                    print(f'No More Pages') # Gives a clean break between Process ID

        try:   
            df.reset_index(drop=True, inplace=True)
            df = df[1:] # Take the data less the header row

            # Remove rows that are not required in the dataframe
            df = df[df[0] != 'ISAM']
            df = df[df[0] != 'Frame Source Frame FTS']
            # Split string into columns
            df = pd.DataFrame(df[0].str.split(' ',2).tolist(),
                                columns = ['Frames','ORIGINATOR', 'NUMBER'])
            df = df.loc[:,['Frames']] # Gives all the rows but only the Frames Column
            df = df['Frames'].value_counts() # Gives the ISAM Number and the count of entries of the ISAM Number
            # print(df.plot())
            df.to_excel(writer, sheet_name= str(process_x)) # Write worksheet to the XLSX workbook

        except (UnboundLocalError, KeyError):
            print('Not an ProcessID or No Information')
            continue # Use this to by-pass a Process ID that fails to give informaion


    writer.save()

    driver.quit()
    return


if __name__ == "__main__":
    main_function()