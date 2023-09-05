import ply.yacc as yacc
from minilex import tokens

GlobalEnv = {}

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),            # Unary minus operator
)

BuiltinBinaryOperators = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
    '<' : lambda x,y: x<y,
    '<=' : lambda x,y: x<=y,
    '>' : lambda x,y: x>y,
    '>=' : lambda x,y: x>=y,
    '==' : lambda x,y : x==y
}

def p_program(p):
    '''program : expression
               | assignment'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ID ASSIGN NUMBER'''
    GlobalEnv[p[1]] = p[3]

def p_expression_lookup(p):
    'expression : ID'
    p[0] = GlobalEnv.get(p[1])
    if p[0] is None:
        raise Exception(f'Undefined reference {p[1]}')

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression'''
    p[0] = BuiltinBinaryOperators[p[2]](p[1], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc(start='program')

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
