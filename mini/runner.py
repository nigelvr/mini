import sys
from .minienv import BasicEnvironment, printenv
from .miniparse import parser

def run(program : str):
    return parser.parse(program).emit(BasicEnvironment)

def run_from_path(filepath : str):
    with open(filepath, 'r') as fd:
        return run(fd.read())
