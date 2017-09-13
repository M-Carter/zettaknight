#!/usr/bin/python
# -*- coding: utf-8 -*-

#    Copyright (c) 2015-2016 Matthew Carter, Ralph M Goodberlet.
#
#    This file is part of Zettaknight.
#
#    Zettaknight is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Zettaknight is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Zettaknight.  If not, see <http://www.gnu.org/licenses/>.
#

# Import python libs

import sys
import yaml
import os
import shutil
import argparse
import types
import inspect
import time
import logging
import importlib
import six

from zkmods.Logger import Logger
from zkmods.Daemon import Daemon

import zkmods.zettaknight_globs as globs
import zkmods.zettaknight_zpool
import zkmods.zettaknight_utils
import zkmods.zettaknight_zfs
import zkmods.zettaknight_recover
import zkmods.zettaknight_ldap
import zkmods.zettaknight_check
import zkmods.zk_env

def help(methods, *args):

    ignore_list = [ 'pipe_this2', 'strip_input', 'mm_post', 'printcolors', 'pipe_this', 'mail_out', 'argparsing', 'replace_string', 'query_yes_no', 'parse_output', 'create_store', 'check_quiet', 'create_kwargs_from_args', 'query_return_list', 'query_return_item', 'spawn_job', 'update_crond', 'update_cron' ]
    command_list = []
    cmd_out = "Zettaknight includes the following callable methods.  To get information about a specific command,run \nzettaknight help <command>\n\n"
    for name in methods.keys():
        if isinstance(methods[name], types.FunctionType):
            if name not in ignore_list:
                command_list.append(name)


if __name__=="__main__":

    parser=argparse.ArgumentParser()
    parser.add_argument('zk_function')
    parser.add_argument('zk_args', nargs='+')
    parser.add_argument('-l', '--level', type=str, default='INFO', help="log level, acceptable is ('DEBUG', 'INFO', 'WARNING', 'CRITICAL')")
    parser.add_argument('-m', '--mail_output', action='store_true', default=False, help='mail the contents of the run')
    parser.add_argument('-e', '--mail_error', action='store_true', default=False, help='mail the contents of the run only if an error is recieved')

    opts = parser.parse_args()
    _args = vars(opts)
    print _args
    
    for item in list(sys.modules):
        if 'zkmods' in item:
            print item
    
    #print globals()
    
    '''
    methods = globals().copy()
    methods.update(locals())
    
    for name in methods.keys():
        if isinstance(methods[name], types.FunctionType):
            print methods[name]
        if isinstance(methods[name], types.ModuleType):
            print methods[name]
            print(dir(methods[name]))
    #print inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    
    '''
    
    #start a module wide instances
    #logging_base = logging.getLogger()
    #set_logging(logging_base) 
    
    
    _modules = globs.modules
    _functions = globs.functions
    
    functions = []
    for module in _modules:
        print module
        #mod = importlib.import_module(module)
        mod = __import__(module, globals={"__name__": __name__})
        globals()[mod] = mod
        func = inspect.getmembers(mod, inspect.isfunction)
        functions = functions + func
        
    _functions = functions
    #print globals()
    #print _functions
    
    try:
        dummy_function()
    except Exception as e:
        print e
        pass
    
    try:
        mod.dummy_function()
    except Exception as e:
        print e
        pass
        
    try:
        modules.zk_env.dummy_function()
    except Exception as e:
        print e
        pass
        
    def _get_all_functions_in_modules(modules=_modules):
        '''
        takes in a list of modules and returns a list of all
        imported functions in a tuple format [(func_name, function object), (..., ...)...]
        '''

        functions = []
        for module in modules:
            mod = importlib.import_module(module)
            func = inspect.getmembers(mod, inspect.isfunction)
            functions = functions + func
            
        _functions = functions
        
        
    def _get_function_executable(function):
        '''
        parses the output from _get_all_functions_in_modules and returns an executable
        for a function that matches the input string function
        '''

        #if no match is found, None is returned
        ret = None
        
        for f in _functions:
            if str(f[0]) == str(function):
                ret = f[1]

        return ret