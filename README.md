# Python Caller ID Tracking

## Setup

### Set the serial port

Edit the app.py and replace the *SERIAL_PORT* line so that it points to the serial port on your system where the 
modem is.

```
SERIAL_PORT = '/dev/ttyS0'
```

### Create the sqlite3 database

Create the database if needed

```
sqlite3 calls.db
```

Create single table to store all the calls

```
CREATE TABLE CALLS(ID INTEGER PRIMARY KEY AUTOINCREMENT, TIMESTAMP INT, NUMBER TEXT, NAME TEXT);
```

## Running

The script must be run with permissions to access the serial port.  This can either be done by running the script as 'root' or adding yourself to the 'dialout' group (most likely)


## Requirments

This runs (at least on my system) in python 2.7.6 and uses sqlite3.  It uses the pyserial module, which came included with my distro.  So nothing additional, really, should be needed.


