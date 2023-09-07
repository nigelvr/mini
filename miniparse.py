import ply.yacc as yacc
from pprint import pprint
from minilex import tokens
from miniast import (
    FuncCallAST,
    FuncdefAST,
    IdentAST,
    NumberAST,
    BinopAST,
    UnaryAST,
    AssignmentAST
)

precedence = (
    ('nonassoc', 'LT'),  # Nonassociative operators
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS')
)

BasicEnvironment = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
    '<' : lambda x,y: x<y,
}

def printenv():
    print('---Global Environment---')
    pprint(BasicEnvironment)
    print('------------------------')

def p_program(p):
    '''program : assignment funcdef expression'''
    # exec the assignment
    p[1].emit(BasicEnvironment)
    # exec the funcdef
    p[2].emit(BasicEnvironment)

    p[0] = p[3]

def p_funcdef(p):
    'funcdef : FUNC ID LPAREN ID RPAREN LSQB funcpart SEMICOL RSQB'
    funcname = p[2]
    argname = p[4]
    expr = p[7]

    p[0] = FuncdefAST(funcname, argname, expr)

def p_funcpart(p):
    'funcpart : RET expression'
    p[0] = p[2]

def p_assignment(p):
    'assignment : ID ASSIGN expression SEMICOL'
    ident = p[1]
    expr = p[3]
    p[0] = AssignmentAST(ident, expr)

def p_expression_funccall(p):
    'expression : ID LPAREN expression RPAREN'
    funcname = p[1]
    arg = p[3]
    p[0] = FuncCallAST(funcname, arg)

def p_expression_lookup(p):
    'expression : ID'
    p[0] = IdentAST(p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression LT expression'''
    p[0] = BinopAST(p[2], p[1], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = UnaryAST('-', p[2])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = NumberAST(p[1])

# Error rule for syntax errors
def p_error(p):
    raise Exception("Syntax error in input!")

# Build the parser
parser = yacc.yacc(start='program')

with open('./example/ex0.mini', 'r') as fd:
    result = parser.parse(fd.read())
    print(result.emit(BasicEnvironment))