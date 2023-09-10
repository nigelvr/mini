import ply.yacc as yacc
from pprint import pprint
from minilex import tokens
from miniast import (
    AST,
    FuncCallAST,
    FuncdefAST,
    IdentAST,
    NumberAST,
    BinopAST,
    UnaryAST,
    AssignmentAST,
    ReturnAST,
    IfAST
)

precedence = (
    ('nonassoc', 'LEQ', 'GEQ', 'AND'),  # Nonassociative operators
    ('left', 'GT', 'LT'),
    ('left', 'EQUALS', 'OR'),
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
    '<=' : lambda x,y : x <= y,
    '>' : lambda x,y : x > y,
    '>=' : lambda x,y: x >= y,
    '==' : lambda x,y : x==y,
    'or' : lambda x,y : x or y,
    'and' : lambda x,y : x and y
}

def printenv():
    print('---Global Environment---')
    pprint(BasicEnvironment)
    print('------------------------')

def flatten(L, class_instance, cond = lambda x : True):
    flat = []
    for x in L:
        if isinstance(x, class_instance) and cond(x):
            flat.append(x)
        elif isinstance(x, list):
            flat += flatten(x, class_instance)
    return flat

def p_program(p):
    '''program : preprog expression
               | expression'''
    preprog = p[1] if len(p) == 3 else []
    print(f'preprog : {preprog}')
    for preprog_block in preprog:
        preprog_block.emit(BasicEnvironment)
    
    p[0] = p[len(p)-1]

def p_preprog(p):
    '''preprog : assignment
               | funcdef
               | preprog assignment
               | preprog funcdef'''
    p[0] = flatten(p[1:], AST)

def p_funcdef(p):
    '''funcdef : FUNC ID LPAREN arglist RPAREN OPBR funcbody CLBR
               | FUNC ID LPAREN arglist RPAREN OPBR CLBR
               | FUNC ID LPAREN RPAREN OPBR funcbody CLBR
               | FUNC ID LPAREN RPAREN OPBR CLBR'''

    funcname = p[2]
    arglist = []
    funcbody = []

    if isinstance(p[4], list): # we have an arglist
        arglist = p[4]

    if isinstance(p[len(p)-2], list): # we have a function body
        funcbody = p[len(p)-2]

    p[0] = FuncdefAST(funcname, arglist, funcbody)

def p_arglist(p):
    '''arglist : ID
               | arglist COMMA ID'''
    p[0] = flatten(p[1:], str, lambda x : x != ',')

def p_funcbody(p):
    '''funcbody : funcpart
                | funcbody funcpart'''
    p[0] = flatten(p[1:], AST)

def p_funcpart(p):
    '''funcpart : ret
                | assignment
                | if'''
    p[0] = p[1]

def p_ret(p):
    'ret : RET expression SEMICOL'
    expr = p[2]
    p[0] = ReturnAST(expr)

def p_assignment(p):
    'assignment : ID ASSIGN expression SEMICOL'
    ident = p[1]
    expr = p[3]
    p[0] = AssignmentAST(ident, expr)

def p_if(p):
    'if : IF LPAREN expression RPAREN OPBR funcbody CLBR'
    cond = p[3]
    body = p[6]
    p[0] = IfAST(cond, body)

def p_expression_funccall(p):
    'expression : ID LPAREN exprlist RPAREN'
    funcname = p[1]
    exprlist = p[3]
    p[0] = FuncCallAST(funcname, exprlist)

def p_exprlist(p):
    '''exprlist : expression
                | exprlist COMMA expression'''
    p[0] = flatten(p[1:], AST)

def p_expression_lookup(p):
    'expression : ID'
    p[0] = IdentAST(p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression LT expression
                  | expression LEQ expression
                  | expression GT expression
                  | expression GEQ expression
                  | expression EQUALS expression
                  | expression OR expression
                  | expression AND expression'''
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
    print(p.type)
    raise Exception("Syntax error in input!")

# Build the parser
parser = yacc.yacc(start='program')

print('START')
printenv()
print()

with open('./example/ex0.mini', 'r') as fd:
    result = parser.parse(fd.read())
    print(result.emit(BasicEnvironment))

print()
print('DONE')
printenv()