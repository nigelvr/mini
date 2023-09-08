import ply.lex as lex

reserved = {
    'func' : 'FUNC',
    'return' : 'RET',
    'if' : 'IF',
    'or' : 'OR',
    'and' : 'AND'
}

# List of token names.   This is always required
tokens = (
   'NUMBER',
   'FUNC',
   'RET',
   'IF',
   'OR',
   'AND',
   'ID',
   'SEMICOL',
   'EQUALS',
   'LT',
   'LEQ',
   'GT',
   'GEQ',
   'ASSIGN',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'LSQB',
   'RSQB',
   'COMMA'
)

#t_BINOP = r'\+|-|\*|/'

# Regular expression rules for simple tokens
t_EQUALS = r'=='
t_LEQ = '<='
t_GEQ = '>='
t_ASSIGN = r'='
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LT = r'<'
t_GT = r'>'
t_LSQB = r'{'
t_RSQB = r'}'
t_COMMA = r','
t_SEMICOL = r';'


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


