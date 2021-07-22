# live_full_list_per_processid.py
''' 
    WebScrape HOPS Staging Server
    Process ID Viewer

	Open the process viewer for specific process ID. (Taken from a variables module)
    This code is to pull the full list of Pending ACKs for a Process ID.

    Multiple Process ID can be added for each TOC
    The output is a single XLSX file per TOC, on which there is a single sheet per Process ID

    Edit the variable.py file as required 


    *** I have a unique number of ISAM - How to add a new row to the df with that information
    *** How to list the unique ISAM numbers into a df and append to the main df

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
    # This For loop broken out, as XLSX write was not completing for multiple TOCs
    for x in TOC:
        controller(x)
    print('Task Complete.')


def controller(x):
    system('cls')  # Clear the Console for ease of viewing
    today = strftime("%Y_%m_%d-%H_%M_%S")  # Gives initial a date time stamp
    the_day = strftime('%Y_%m_%d')  # Give a date stamp
    no_id_found = []
    pending_acks_there = []
    # Setup Chrome Browser
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=options)  # Put your webdriver into PATH
    # I like smaller windows, ** Don't make it too small though
    driver.set_window_size(600, 700)
    print(f'Live - {x}')

    # Create the Live url path here from the dict
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

    # Create an XLSX workbook per TOC
    name_file = str(dir + '/' + x + '_' + today +'.xlsx')
    writer = pd.ExcelWriter(name_file, engine='xlsxwriter')

    # Loop through the ISAMs
    # Choose the TOC ISAM list from the dict
    process_list = list(id_Live_dict[x])
    print(process_list)

    # Get to the complete table of Info for an ISAM
    for process_x in process_list:
        print(process_x)
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
                # print(
                #     f'There is no "Search Result" for Process ID {process_x}')
                no_id_found.append(process_x)
            Event().wait(2)
            pending_acks_there.append(process_x)
            

            tagged = driver.find_element_by_id('missingAcks').text
            s = StringIO(tagged)
            df = pd.read_table(s, header= None)
            # print(df)
            # Loop over each other page for the ISAM
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
                print("No pages") # In case there isn't a table for that ISAM
                continue
        except NoSuchElementException:
                    print(f'No More Pages') # Gives a clean break between ISAM

        try:   
            name = str(process_x)
            df.reset_index(drop=True, inplace=True)
            df = df[1:] #take the data less the header row
 
            # Remove Rows
            df = df[df[0] != 'ISAM']
            df = df[df[0] != 'Frame Source Frame FTS']
            # Split string in columns
            df = pd.DataFrame(df[0].str.split(' ',2).tolist(),
                                columns = ['ID','ORIGINATOR', 'NUMBER'])
            # Get Unique List
            df_names = {k: v for (k, v) in df.groupby('ID')}
            df_uniques = pd.DataFrame(df_names.items(), columns=['ID', 'ORIGINATOR'])
            df = df.append(df_uniques)

            # Count the Unique ISAM Numbers
            no_of_isam = df['ID'].nunique()
            dfcount = pd.DataFrame({'ID':['Number of Unique ISAM'], 'ORIGINATOR': [no_of_isam]})
            df = df.append(dfcount)

            print(f'Number of ISAM {no_of_isam}')
            df.to_excel(writer, sheet_name= name) # Write Sheet to the Excel Workbook

        except (UnboundLocalError, KeyError):
            print('Not an ProcessID or No Information')
            continue # Use this to pass an ISAM that fails to give informaion


    writer.save()

    driver.quit()
    return


if __name__ == "__main__":
    main_function()
