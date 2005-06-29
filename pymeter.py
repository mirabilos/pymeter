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


import os
import sys
import time
from pymeterlib import *


#get the current working directory
working_dir = os.getcwd()
#set the working directory in the Utils module
Utils.working_dir = working_dir
#check the lock and don't allow multiple versions of PyMeter to run
Utils.check_lock()
#create a new lock file and write the current pid into it
Utils.write_lock(working_dir)

#get configurations from config file and do initialization
config = Config.Config('pymeter.cfg')

#if we are running in daemon mode, update the lock since the pid changes when we daemonize [in Config]
if config.is_daemon:
    Utils.write_lock(working_dir)

#create a list of HostConfig objects and load them up with data
host_configs = [HostConfig.HostConfig(config_section, config) for config_section in config.config_sections]
#get the interval from HostConfig file so we can calculate how long to sleep between collections
interval = config.interval 

#poll for stats in a loop for the life of the program [when in daemon mode]
polling = True
while polling:
    start_time = time.time()
    for host_config in host_configs:
        host_config.host.check_stats()
        try:
            host_config.update_storage()
        except Exception, error:
            sys.stderr.write(str(error) + '\n')
            Utils.log(str(error))
            sys.exit(1)
    end_time = time.time()
    if config.is_daemon:
        #sleep until the collection interval has expired
        expire_time = (interval - (end_time - start_time))
        if expire_time > 0:
            time.sleep(expire_time)
        else:
            Utils.log('WARNING - interval expired before polling was complete')
    else:
        #we don't poll unless we are in daemon mode
        polling = False
