import sys
from minienv import BasicEnvironment, printenv
from miniparse import parser

def run(filepath : str):
    printenv()
    print('-----------------\n')

    ret = None
    with open(filepath, 'r') as fd:
        parsed = parser.parse(fd.read())
        ret = parsed.emit(BasicEnvironment)

    printenv()
    print('-----------------\n')
    return ret
    
if __name__ == '__main__':
    print(run(sys.argv[1]))
