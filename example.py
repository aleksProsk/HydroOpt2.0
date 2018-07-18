import os
from RestrictedPython import compile_restricted
from RestrictedPython import safe_builtins
from datetime import date, timedelta, datetime

def wrapper(user, screen):
    def function():
        print(user, screen)
    return function

lst = []
for i in range(5):
    lst.append(wrapper(i, str(i)))

for i in range(5):
    lst[i]()

for i in range(5):
    lst[i]()


def compile_callbacks_file(source_code, function):
    locals = {}
    byte_code = compile_restricted(
        source=source_code,
        filename='<inline>',
        mode='exec'
    )
    additional_globals = {
        'function': function
    }
    safe_globals = safe_builtins
    safe_globals.update(additional_globals)
    exec(byte_code, safe_globals, locals)
    return locals

s = "def simpleExample(): function()"
functionLst = []
for i in range(5):
    functionLst.append(compile_callbacks_file(s, wrapper(i, i)))
print(functionLst)
for f in functionLst:
    f['simpleExample']()

# dct = compile_callbacks("001")