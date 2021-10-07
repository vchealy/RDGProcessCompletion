# header.py

from os import system

logo = '''
  ___  _____  _   __   ______              _ _              
 / _ \/  __ \| | / /   | ___ \            | (_)             
/ /_\ \ /  \/| |/ /    | |_/ /__ _ __   __| |_ _ __   __ _  
|  _  | |    |    \    |  __/ _ \ '_ \ / _` | | '_ \ / _` | 
| | | | \__/\| |\  \   | | |  __/ | | | (_| | | | | | (_| | 
\_| |_/\____/\_| \_/   \_|  \___|_| |_|\__,_|_|_| |_|\__, | 
                                                      __/ | 
                                                     |___/  
'''


def header(x, process_x):
    # To keep a clean console throughout the run
    system('cls')
    print(logo)
    print(f'Live - {x}')
    print(f'The current Process ID is {process_x}') 



def footer():
    # Gives a finally message
    system('cls')
    print(logo)
    print('Task Complete.\n')