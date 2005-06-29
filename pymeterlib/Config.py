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
import ConfigParser
import Daemon


class Config:
    
    def __init__(self, config_file_name):
        #read the config file        
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_file_name)
        
        #get DEFAULT (global) configurations 
        try: 
            self.interval = self.config.getint('DEFAULT', 'interval')
            self.output_dir = self.config.get('DEFAULT', 'output_dir')
            self.storage_type = self.config.get('DEFAULT', 'storage_type')
            self.is_daemon = False
        except ConfigParser.NoOptionError, error:
            sys.stderr.write('ERROR - config file is missing required option: ' + str(error) + '\n')
            sys.exit(1)
            
        #create a list of section names from the config file (each section corresponds to a host, except DEFAULT)
        self.config_sections = [config_section for config_section in self.config.sections()]
        
        try:
            if self.config.get('DEFAULT', 'run_as_daemon') == 'yes':
                print 'Daemonizing PyMeter ... '
                Daemon.createDaemon()
                self.is_daemon = True
        except ConfigParser.NoOptionError:
            pass
    
    
    def get(self, section_name, item_name):
        return self.config.get(section_name, item_name)
    
    
    def has_option(self, section_name, item_name):
        return self.config.has_option(section_name, item_name)
        