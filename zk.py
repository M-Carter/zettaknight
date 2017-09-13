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

from Logger import Logger
from Daemon import Daemon


import modules.zettaknight_globs
import modules.zettaknight_zpool
import modules.zettaknight_utils
import modules.zettaknight_zfs
import modules.zettaknight_recover
import modules.zettaknight_ldap
import modules.zettaknight_check
import modules.zk_env


#new_functions = inspect.getmember(module, inspect.isfuction)

cglobals = globals().copy()
for name, val in six.iteritems(cglobals):
        if isinstance(val, types.ModuleType):
            print val.__name__
    
print 'functions:', functions
        
def argparsing():
    
    #parser = argparse.ArgumentParser()
    
    #parser.add_argument('function', metavar=('Function', 'F'), nargs='+', help='Zettaknight function to execute.')
    #parser.add_argument('-f', '--foo', nargs='+', help='just display something different')
    #parser.parse_args()
    
    
    return

def help(methods, *args):
    
    ignore_list = [ 'pipe_this2', 'strip_input', 'mm_post', 'printcolors', 'pipe_this', 'mail_out', 'argparsing', 'replace_string', 'query_yes_no', 'parse_output', 'create_store', 'check_quiet', 'create_kwargs_from_args', 'query_return_list', 'query_return_item', 'spawn_job', 'update_crond', 'update_cron' ]
    command_list = []
    cmd_out = "Zettaknight includes the following callable methods.  To get information about a specific command,run \nzettaknight help <command>\n\n"
    for name in methods.keys():
        if isinstance(methods[name], types.FunctionType):
            if name not in ignore_list:
                command_list.append(name)
        
def parse_args(parser):

    zettaknight_globs.subparsers = parser.add_subparsers(help='callable functions for Zettaknight', dest='function')

    parser.add_argument('-l', '--level', type=str, default='INFO', help="log level, acceptable is ('DEBUG', 'INFO', 'WARNING', 'CRITICAL')")
    parser.add_argument('-m', '--mail_output', action='store_true', default=False, help='mail the contents of the run')
    parser.add_argument('-e', '--mail_error', action='store_true', default=False, help='mail the contents of the run only if an error is recieved')
    
    
    
def myfun(a):

    myargs = zettaknight_globs.subparsers.add_parser('myfun', help='this is a test') 
    myargs.add_argument('action', action='store', choices=['start', 'stop', 'restart', 'status'], help='callable function methods')
        
        
if __name__=="__main__":

    # Parse the subcommand argument first
    parser = ArgumentParser(add_help=False)
    parser.add_argument("function", 
                        nargs="?",
                        choices=[arg for arg in globals()],
                        )
    parser.add_argument('--help', action='store_true')
    args, sub_args = parser.parse_known_args(['--help'])

    #start a module wide instances
    logging_base = logging.getLogger()
    parser_base = argparse.ArgumentParser()

    abspath = os.path.realpath(__file__)
    base_dir = os.path.dirname(abspath)

    set_logging(logging_base)
    
    parse_args(parser_base)
    opts = parser_base.parse_args()
    _args = vars(opts)
    #module = __import__(_args['function'])
    #globals()[_args['function']] = module

    #print '\n\n', globals()
    
    funcname = _args['function']
    methods = globals().copy()
    methods.update(locals())
    func = methods.get(funcname)

    run_function(func, )

