# Server Process Confirmation
HOPS Process Viewer

Access each servers process viewer and check for specific process to have completed.

**main.py**  
There is a complete change and this has been removed.
In its place is two scripts, one that is a quick check that the process is valid and second that scrapes and manages the full data.

**Additional modules**  
**auth.py**  
    This allows the user to add their authorisation information without affecting the main code
    This holds the url domains required

**variables.py**  
    Gives the various customisations available to the user.
    Choice of Live or Test Domain
    Choice of TOC, choose all TOCs that Process ID have been supplied. Gives single run through all.
    Process IDs
    Holds the dict to the unique code for each TOC.
    Added a dixt for the Process ID for both domains

**requirements.txt**  
    Holds all the dependencies to install
