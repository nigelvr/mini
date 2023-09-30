import sys
from .minienv import BasicEnvironment, printenv
from .miniparse import parser

def run(program_s : str):
    program_func = parser.parse(program_s).emit()
    return program_func()

def run_from_path(filepath : str):
    with open(filepath, 'r') as fd:
        return run(fd.read())
