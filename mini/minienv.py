from pprint import pprint

BasicEnvironment = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
    '<' : lambda x,y: x<y,
    '<=' : lambda x,y : x <= y,
    '>' : lambda x,y : x > y,
    '>=' : lambda x,y: x >= y,
    '==' : lambda x,y : x==y,
    'or' : lambda x,y : x or y,
    'and' : lambda x,y : x and y,
}

SpecialBuiltins = {
    'print' : print
}

def printenv():
    print('---Global Environment---')
    pprint(BasicEnvironment)
    print('------------------------')
