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

@author: Corey Goldberg
@copyright: (C) 2005 Corey Goldberg
@license: GNU General Public License (GPL)
"""


import sys
import time


class StatLog:
        
    def __init__(self, statlog_name):     
        self.statlog_name = statlog_name
        
        
    def update(self, *values):
        #open file in append mode
        logfile = open(self.statlog_name, 'a')
        #string containg local date/time in locale appropriate representation
        timestring = time.strftime('%x %X', time.localtime())
        #put the stats in a pipe delimited string
        stats = ''.join([str(value) + "|" for value in values])[:-1]
        #write it all out to the log in pipe delimited format
        logfile.write(''.join((timestring, '|', stats, '\n')))
        logfile.close()
            