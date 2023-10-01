import ply.yacc as yacc
from pprint import pprint

from .minilex import tokens
from .miniast import (
    AST,
    FuncCallAST,
    FuncdefAST,
    IdentAST,
    NumberAST,
    ListAST,
    BinopAST,
    UnaryAST,
    AssignmentAST,
    ReturnAST,
    IfElseAST,
    WhileAST,
    ProgramAST
)
from .minienv import BasicEnvironment, printenv

precedence = (
    ('left', 'GT', 'LT', 'LEQ', 'GEQ'),
    ('left', 'EQUALS', 'OR', 'AND'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS', 'UPLUS')
)

'''
Helper functions for emitting ASTs
'''
def flatten(L, class_instance, cond = lambda x : True):
    flat = []
    for x in L:
        if isinstance(x, class_instance) and cond(x):
            flat.append(x)
        elif isinstance(x, list):
            flat += flatten(x, class_instance)
    return flat

def production_to_function(p):
    funcname = p[2]
    arglist = []
    codeblock = []

    if isinstance(p[4], list): # we have an arglist
        arglist = p[4]

    if isinstance(p[len(p)-2], list): # we have a function body
        codeblock = p[len(p)-2]

    return FuncdefAST(funcname, arglist, codeblock)

'''
Production rules
'''
def p_program(p):
    '''program : preprog funcdef
               | funcdef'''
    preprog = p[1] if len(p) == 3 else []
    mainfunc = p[len(p)-1]
    
    if not mainfunc.ismain:
        raise Exception("Final function in program file must be \"main\"")
    
    p[0] = ProgramAST(preprog, mainfunc)

def p_preprog(p):
    '''preprog : assignment
               | funcdef
               | preprog assignment
               | preprog funcdef'''
    p[0] = flatten(p[1:], AST)

def p_funcdef(p):
    '''funcdef : FUNC ID LPAREN arglist RPAREN OPBR codeblock CLBR
               | FUNC ID LPAREN arglist RPAREN OPBR CLBR
               | FUNC ID LPAREN RPAREN OPBR codeblock CLBR
               | FUNC ID LPAREN RPAREN OPBR CLBR'''
    p[0] = production_to_function(p)

def p_arglist(p):
    '''arglist : ID
               | arglist COMMA ID'''
    p[0] = flatten(p[1:], str, lambda x : x != ',')

def p_codeblock(p):
    '''codeblock : funcpart
                 | codeblock funcpart'''
    p[0] = flatten(p[1:], AST)

def p_funcpart(p):
    '''funcpart : ret
                | assignment
                | branch
                | proccall
                | while'''
    p[0] = p[1]

def p_ret(p):
    'ret : RET expression SEMICOL'
    expr = p[2]
    p[0] = ReturnAST(expr)

def p_assignment(p):
    'assignment : ident ASSIGN expression SEMICOL'
    ident = p[1]
    expr = p[3]
    p[0] = AssignmentAST(ident, expr)

def p_branch(p):
    '''branch : IF LPAREN expression RPAREN OPBR codeblock CLBR
              | IF LPAREN expression RPAREN OPBR codeblock CLBR ELSE OPBR codeblock CLBR'''
    cond = p[3]
    ifconseq = p[6]
    elseconseq = [] if len(p) == 8 else p[10]
    p[0] = IfElseAST(cond, ifconseq, elseconseq)

def p_expression_proccall(p):
    '''proccall : ID LPAREN exprlist RPAREN SEMICOL
                  | ID LPAREN RPAREN SEMICOL'''
    funcname = p[1]
    exprlist = p[3] if len(p) == 6 else []
    p[0] = FuncCallAST(funcname, exprlist)

def p_while(p):
    '''while : WHILE LPAREN expression RPAREN OPBR codeblock CLBR'''
    cond = p[3]
    body = p[6]
    p[0] = WhileAST(cond, body)

def p_expression_funccall(p):
    '''expression : ID LPAREN exprlist RPAREN
                  | ID LPAREN RPAREN'''
    funcname = p[1]
    exprlist = p[3] if len(p) == 5 else []
    p[0] = FuncCallAST(funcname, exprlist)

def p_expression_list(p):
    '''expression : LSQB RSQB
                  | LSQB exprlist RSQB'''
    L = [] if len(p) == 3 else p[2]
    p[0] = ListAST(L)

def p_exprlist(p):
    '''exprlist : expression
                | exprlist COMMA expression'''
    p[0] = flatten(p[1:], AST)

def p_expression_lookup(p):
    '''expression : ident'''
    p[0] = p[1]

def p_ident(p):
    '''ident : ID
             | ID subscript_list'''
    ident = p[1]
    subscript_list = [] if len(p) == 2 else p[2]
    p[0] = IdentAST(ident, subscript_list)

def p_subscript_list(p):
    '''subscript_list : LSQB expression RSQB
                      | subscript_list LSQB expression RSQB'''
    L = []
    if len(p) == 4:
        L += [p[2]]
    else:
        L = p[1] + [p[3]]
    p[0] = flatten(L, AST)

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

def p_expr_uplus(p):
    'expression : PLUS expression %prec UPLUS'
    p[0] = UnaryAST('+', p[2])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = NumberAST(p[1])

# Error rule for syntax errors
def p_error(p):
    print(p.type)
    raise Exception("Syntax error in input!")

# Build the parser
parser = yacc.yacc(start='program')
