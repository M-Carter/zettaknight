#!/usr/bin/python

import importlib
import inspect
import modules.zettaknight_globs

_libraries = modules.zettaknight_globs.modules
_modules = modules.zettaknight_globs.modules
_functions = modules.zettaknight_globs.functions
    
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