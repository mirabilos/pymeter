#!/usr/bin/env python


#  Copyright 2005 Corey Goldberg (corey@goldb.org)
#
#  This file is part of PyMeter.
#
#  PyMeter is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  PyMeter is distributed in the hope that it will be useful,
#  but without any warranty; without even the implied warranty of
#  merchantability or fitness for a particular purpose.  See the
#  GNU General Public License for more details.

 
"""
Utilities used with PyMeter.

@author: Corey Goldberg
@copyright: (C) 2005 Corey Goldberg
@license: GNU General Public License (GPL)
"""


import os
import sys
import time


def write_lock(working_dir):
    """create a new lock file and write the current pid into it"""
    try:
        file_write = open(working_dir + '/pymeter.pid', 'w')
        file_write.write(str(os.getpid()))
        file_write.close() 
    except IOError:
        sys.stderr.write("ERROR - PyMeter needs write permission to it's working directory and .pid file!\n")
        sys.exit(1)


def check_lock():
    """check the lock and don't allow multiple versions of PyMeter to run"""
    try:
        file_read = open('pymeter.pid', 'r')
        saved_pid = int(file_read.read())
        file_read.close() 
        try:
            #send the saved pid a dummy kill signal (0)
            #If the process does not exist, an exception is thrown
            os.kill(saved_pid, 0)
        except OSError, error:
            if error.errno == 3:
                pass
            else:
                #if PyMeter is running as root, and a second version tries to start as non-root,
                #the dummy kill signal throws an exception "[Errno 1] Operation not permitted"
                #instead of the "[Errno 3] No such process" we are expecting.
                sys.stderr.write('ERROR - Another instance of PyMeter is already running!\n')
                sys.exit(1)
        else:
            sys.stderr.write('ERROR - Another instance of PyMeter is already running!\n')
            sys.exit(1)
    except IOError:
        #this happens when the lock file doesn't exist, so we can't open it in read mode
        #if the lock file doesn't exist, it is definitely not locked.
        pass


working_dir = './'
def log(text):
    """write text out to the log file with a timestamp"""
    logfile = open(working_dir + '/pymeter.log', 'a')
    #string containg local date/time in locale appropriate representation
    timestring = time.strftime('%x %X', time.localtime())
    logfile.write(''.join((timestring, ' >> ', text, '\n')))
    logfile.close()
    