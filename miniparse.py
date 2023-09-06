import ply.yacc as yacc
from minilex import tokens

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

class AST:
    def __init__(self, root, children):
        self.root = root
        self.children = children

    def emit(self, env):
        pass

class UnaryAST(AST):
    def __init__(self, op, value):
        super().__init__(op, [value])

    def emit(self, env):
        if self.root == '+':
            return self.children[0].emit(env)
        elif self.root == '-':
            return -self.children[0].emit(env)

class BinopAST(AST):
    def __init__(self, op, p1, p2):
        super().__init__(op, [p1, p2])
    
    def emit(self, env):
        return env[self.root](
            self.children[0].emit(env),
            self.children[1].emit(env)
        )

class NumberAST(AST):
    def __init__(self, number):
        super().__init__(number, [])

    def negate(self):
        self.root *= -1
        return self
    
    def emit(self, env=None):
        return self.root
    
class FuncdefAST(AST):
    def __init__(self, funcname, argname, expr):
        super().__init__(funcname, [argname, expr])

    def emit(self, env):
        env[self.root] = self
        return self

class FuncCallAST(AST):
    def __init__(self, funcname, argvalue):
        super().__init__(funcname, [argvalue])

    def emit(self, env):
        func = env[self.root]
        argname = func.children[0]
        env[argname] = self.children[0]
        return func.children[1].emit(env)

class IdentAST(AST):
    def __init__(self, ident):
        super().__init__(ident, [])
    
    def emit(self, env):
        return env[self.root]

def p_program(p):
    '''program : expression
               | funcdef'''
    p[0] = p[1]

def p_funcdef(p):
    'funcdef : FUNC ID LPAREN ID RPAREN LSQB RET exprfunc foo(x) { return x+3 }ession RSQB'
    funcname = p[2]
    argname = p[4]
    expr = p[8]
    p[0] = FuncdefAST(funcname, argname, expr)

def p_expression_funccall(p):
    'expression : ID LPAREN NUMBER RPAREN'
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
