# Server Process Confirmation
HOPS Process Viewer

Access each servers process viewer and check for specific process to have completed.

**main.py**  
    The main code with editable sections, this is improved in other code writes after this.  
    But will remain as is for reference on where I initially wrote

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
