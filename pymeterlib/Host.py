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


class Host:
        
    """Unix-like Host.
        
    @ivar plugins: Instances of plugin objects to run for stat checks
    @ivar stat_labels: Labels (names) of the stats to be checked
    @ivar last_stats: Value of the stat (or list of stats) from the last check
    @ivar stored_stats: List of stats collected since enabling storage or last flush
    @ivar storage_enabled: Indication if internal storage of stats is enabled (boolean)
    """
        
    def __init__(self, *plugins):
        """
            
        @param plugins: Instances of plugin objects to run for stat checks (arbitrary number of arguments)
        """        
        self.plugins = plugins
        self.stat_labels = []
        self.stored_stats = []
        self.last_stats = []
        self.stat_labels = [plug.label for plug in plugins]
        self.storage_enabled = False
        
        
    def check_stats(self):
        """Run plugin commands on the local host.
            
        @return: Stats 
        @rtype: List of strings
        """
        plugin_stats = []
        for plug in self.plugins:
            #execute the command as a subprocess and return file objects (child_stdin, child_stdout_and_stderr)
            cmd = os.popen4(plug.command)
            #read contents of the file object (child_stdout_and_stderr) until EOF
            cmd_output = cmd[1].read()
            plugin_stats.append(plug.format_output(cmd_output))
        self.last_stats = plugin_stats
        if self.storage_enabled:
            self.stored_stats.append(plugin_stats)
        return plugin_stats
        
        
    def flush_stats(self):
        """Flush (clear) any stats stored in the object."""
        self.stored_stats = []
        self.last_stats = []
        
        
    def enable_storage(self):
        """Enable internal storage of stats.  (Disabled by default)"""
        self.storage_enabled = True
        
        
    def disable_storage(self):
        """Disable internal storage of stats and flush any existing storage.  (Disabled by default)"""
        self.storage_enabled = True
        self.flush_stats()
        
    