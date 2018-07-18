import os
from RestrictedPython import compile_restricted
from RestrictedPython import safe_builtins
from datetime import date, timedelta, datetime

def compile_callbacks_file(source_code, getScreenVariables):
    locals = {}
    byte_code = compile_restricted(
        source = source_code,
        filename = '<inline>',
        mode = 'exec'
    )
    additional_globals = {
        'date': date, 'timedelta': timedelta, 'datetime': datetime, 'getScreenVariables': getScreenVariables
    }
    safe_globals = safe_builtins
    safe_globals.update(additional_globals)
    exec(byte_code, safe_globals, locals)
    return locals

def compile_callbacks(uid, getScreenVariables):
    path = "user" + uid + "/scripts/dash/screens/"
    screenNames = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            screenNames.append(os.path.join(name))
    functions = {}
    for screenName in screenNames:
        f = open(path + screenName + "/callbacks.py", "r")
        s = f.read()
        functionLst = compile_callbacks_file(s, getScreenVariables)
        functions[screenName] = functionLst
    return functions

#dct = compile_callbacks("001")