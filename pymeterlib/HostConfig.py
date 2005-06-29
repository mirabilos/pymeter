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


import os.path
import re
import sys
import RRD
import StatLog  
import Host
import RemoteHost
import PluginRegistry
import Utils
from plugins import *
        

class HostConfig:
    
    def __init__(self, host_config_section, config):
        self.rrd = None
        self.statlog = None
        
        #assign a reference to Config as an instance variable
        self.config = config
        
        #get configurations for individual host
        self.section_name = host_config_section
        self.host_type = self.config.get(self.section_name, 'host_type')
        self.plugin_names = re.split(',\s*', self.config.get(self.section_name, 'plugins'))
        #get a list of of plugin objects we will need
        self.plugin_objects = self.__lookup_plugins(self.host_type)
        
        #setup storage for stats (using either RRD (Round Robin Database) or text/log file storage) 
        self.__setup_storage()
        
        #instantiate a Host object and assign a reference to it as an instance variable
        if self.config.has_option(host_config_section, 'remote_connect'):
            connection_params = self.config.get(self.section_name, 'remote_connect').split('|')
            if len(connection_params) != 5:
                raise Exception, 'Invalid format for remote_connect parameters.  Must contain 5 pipe delimited fields'
            self.host = RemoteHost.RemoteHost(connection_params[0], connection_params[1], connection_params[2], 
                connection_params[3], connection_params[4], *self.plugin_objects)
        #if no remote_connect is specified, we assume it is the local host
        else:
            self.host = Host.Host(*self.plugin_objects)


    def __lookup_plugins(self, host_type):
        #copy the list of plugin names to a new list (take a slice the size of the entire list) so we can modify it
        plugin_lookup_names = self.plugin_names[:]
        #strip any data source types (pipe and anything after it) from the plugin names, so we have a clean list for lookups
        plugin_lookup_names = [plugin_lookup_name.split('|')[0] for plugin_lookup_name in plugin_lookup_names]   
            
        if host_type == 'linux':
            #use the keys (plugin names) to lookup plugins in the dictionary and instantiate the ones we need into a list
            return [PluginRegistry.plugin_dict_linux[plugin_lookup_name]() for plugin_lookup_name in plugin_lookup_names]
        if host_type == 'solaris':               
            #use the keys (plugin names) to lookup plugins in the dictionary and instantiate the ones we need into a list
            return [PluginRegistry.plugin_dict_solaris[plugin_lookup_name]() for plugin_lookup_name in plugin_lookup_names]


    def __setup_storage(self):
        #setup storage for stats using either RRD (Round Robin Database) or text/log file storage 
        if self.config.storage_type == "rrd":
            rrd_name = self.section_name + '.rrd'
            #instantiate an RRD object so we can use an RRD (Round Robin Database) for data storage
            self.rrd = RRD.RRD(self.config.output_dir + rrd_name)
            
            #in RRDtool, each Data Source has a DST (Data Source Type).  We default to "GAUGE", but allow a user to specify
            #a different DST by appending it to the plugin name after a pipe (example: NetworkBytesSent|COUNTER).
            #so we separate the names and types and create a list of tuples containing these
            ds_names_and_types = []
            for plugin_name in self.plugin_names:
                #if there is a pipe in the plugin name, parse the name and type
                if '|' in plugin_name:
                    ds_names_and_types.append((plugin_name.split('|')[0], plugin_name.split('|')[1])) 
                #if no pipe is present, default to a GAUGE DST
                else:
                    ds_names_and_types.append((plugin_name, 'GAUGE')) 
            
            #build the data source list to create our RRD with (using plugin names for data source names)
            data_sources = [(plugin_name, data_source_type, 'U', 'U') for plugin_name, data_source_type in ds_names_and_types]
            #only create the RRD if it does not exist      
            if not os.path.isfile(self.config.output_dir + rrd_name):
                try:
                    self.rrd.create_rrd(self.config.interval, data_sources)
                except RRD.RRDException, error:
                    sys.stderr.write(str(error) + '\n')
                    Utils.log(str(error))
                    sys.exit(1)
        #if we don't use an RRD, we use a text/log file for data storage
        else:
            statlog_name = self.section_name + '.log'
            #instantiate a StatLog object so we can use a text/log file for data storage
            self.statlog = StatLog.StatLog(self.config.output_dir + statlog_name)
            

    def update_storage(self):
        if self.config.storage_type == "rrd":
            self.rrd.update(*self.host.last_stats)
        else:
            self.statlog.update(*self.host.last_stats)



               
        
            
            
            
        
        
