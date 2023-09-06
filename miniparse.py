import ply.yacc as yacc
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



def p_program(p):
    '''program : expression
               | funcdef
               | assignment'''
    p[0] = p[1]

def p_funcdef(p):
    'funcdef : FUNC ID LPAREN ID RPAREN LSQB RET expression RSQB'
    funcname = p[2]
    argname = p[4]
    expr = p[8]
    p[0] = FuncdefAST(funcname, argname, expr)

def p_assignment(p):
    'assignment : ID ASSIGN expression'
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

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result.emit(BasicEnvironment))
