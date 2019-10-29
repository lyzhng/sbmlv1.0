# Code written by Lily Zhong

import sys
import ply.lex as lex
import ply.yacc as yacc

def print_alot(p):
    print("P:", p)
    print("DIR:", dir(p))
    print("SLICE", p.slice)
    print("STACK", p.stack)

tokens = (
    'INTEGER',
    'REAL',
    'BOOLEAN',
    'STRING',
    'LPAREN',
    'RPAREN',
    'HASH',
    'LBRACKET',
    'RBRACKET',
    'INTDIVOP',
    'MULOP',
    'EXPOP',
    'DIVOP',
    'MODOP',
    'PLUSOP',
    'MINUSOP',
    'INOP',
    'NOTOP',
    'CONJUNCTIONOP',
    'DISJUNCTIONOP',
    'LTOP',
    'LTEOP',
    'EQOP',
    'NEQOP',
    'GTEOP',
    'GTOP',
    'CONCATOP',
    'COMMA',
) 

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_HASH = r'\#'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_DIVOP = r'\/'
t_MULOP = r'\*'
t_EXPOP = r'\*{2}'
t_INTDIVOP = r'div'
t_MODOP = r'mod'
t_PLUSOP = r'\+'
t_MINUSOP = r'\-'
t_INOP = r'in'
t_NOTOP = r'not'
t_CONJUNCTIONOP = r'andalso'
t_DISJUNCTIONOP = r'orelse'
t_LTOP = r'\<'
t_LTEOP = r'\<\='
t_EQOP = r'\={2}'
t_NEQOP = r'\<\>'
t_GTEOP = r'\>\='
t_GTOP = r'\>'
t_CONCATOP = r'\:{2}'
t_COMMA = r'\,'

t_ignore = ' \t'

def t_INTEGER(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t

# Fix me
def t_REAL(t):
    r'testing'
    t.value = float(t.value)
    return t

# Is this a problem?
def t_BOOLEAN(t):
    r'True|False'
    t.value = True if t.value == 'True' else False
    return t

def t_STRING(t):
    r'\'[^\']*\'|\"[^\"]*\"'
    t.value = t.value
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("SYNTAX ERROR: %s at %d" % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)
    sys.exit()

lexer = lex.lex()

# Parsing rules

# Mathematical expression

def p_proposition_expression(p):
    'statement : expression'
    p[0] = p[1]

def p_proposition_math(p):
    '''
    expression : expression PLUSOP expression
            |    expression MINUSOP expression
            |    expression MULOP expression
            |    expression DIVOP expression
            |    expression MODOP expression
            |    expression INTDIVOP expression
            |    expression EXPOP expression
    '''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = float(p[1] / p[3])
    elif p[2] == 'mod':
        p[0] = p[1] % p[3]
    elif p[2] == 'div':
        p[0] = int(p[1] / p[3])
    elif p[2] == '**':
        p[0] = pow(p[1], p[3])

def p_proposition_number(p):
    '''
    expression : INTEGER
            |    REAL
            |    BOOLEAN
    '''
    p[0] = p[1]

def p_proposition_conjunction(p):
    'expression : expression CONJUNCTIONOP expression'
    p[0] = True if p[1] and p[3] else False

def p_proposition_disjunction(p):
    'expression : expression DISJUNCTIONOP expression'
    p[0] = True if p[1] or p[3] else False

def p_proposition_parenthetical(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_proposition_brackets(p):
    'expression : LBRACKET expression RBRACKET'
    p[0] = p[2]
    
# def p_proposition_list(p):
#     '''
#     expression : LBRACKET items RBRACKET
#     '''
    

def p_error(p):
    print("SEMANTIC ERROR %s" % (p))
    sys.exit()

precedence = (
    ('left', 'GTOP'),
    ('left', 'GTEOP'),
    ('left', 'NEQOP'),
    ('left', 'EQOP'),
    ('left', 'LTEOP'),
    ('left', 'LTOP'),
    ('left', 'CONJUNCTIONOP', 'DISJUNCTIONOP'),
    ('left', 'NOTOP'),
    ('right', 'CONCATOP'),
    ('left', 'INOP'),
    ('left', 'PLUSOP', 'MINUSOP'),
    ('left', 'INTDIVOP', 'MODOP'),
    ('left', 'MULOP', 'DIVOP'),
    ('right', 'EXPOP'),
    # a[b],
    # i(tuple),
    # tuple constructor,
    ('left', 'LPAREN', 'RPAREN'),
)

parser = yacc.yacc()

while True:
    try:
        s = input("Enter a proposition: ")
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s, debug=True)
    print("RESULT:", result)