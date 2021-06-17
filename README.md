# RDGHOPSProcess
HOPS Process Viewer

Access each TOC HOPS and look at the process viewer for specific process ID.

Allowing the user to know whether an ISAM has picked up and successfully processed the
message or whether further action is required.  

main.py  
    Edit the sections at line 40+ to determine which domain is requested

Additional modules

auth.py
    This allows the user to add their authorisation information without affecting the main code
    This holds the url domains required

variables.py
    Gives the various customisations available to the user.
    Choice of Live or Test Domain
    Choice of TOC
    Process IDs
    Holds the dict to the unique code for each TOC.

requirements.txt
    Holds all the dependencies to install
