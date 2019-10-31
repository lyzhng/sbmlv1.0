# Code written by Lily Zhong

import sys
import ply.lex as lex
import ply.yacc as yacc

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
    'SEMICOLON'
) 

t_LPAREN = r'\('
t_RPAREN = r'\)'
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
t_SEMICOLON = r'\;'

t_ignore = ' \t'

## Data types

def t_REAL(t):
    r'(([-]?([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)([eE][-]?[0-9]+)?))'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_BOOLEAN(t):
    r'True|False'
    t.value = 'True' == t.value
    return t

def t_STRING(t):
    r'\'[^\']*\'|\"[^\"]*\"'
    t.value = t.value[1:-1]
    return t

def t_HASH(t):
    r'\#\([^\(\)]+\)'
    t.value = t.value
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

## Lexing error

def t_error(t):
    print("SYNTAX ERROR")
    t.lexer.skip(1)

lexer = lex.lex()

## PARSING

## General

def p_proposition_expr(p):
    'stmt : expr SEMICOLON'
    p[0] = p[1]

def p_proposition_brackets(p):
    'expr : LBRACKET expr RBRACKET'
    p[0] = p[2]

## Tuple functions

def p_proposition_settup(p):
    '''
    expr : tup
         | tupindex
    '''
    p[0] = p[1]

def p_proposition_tupindex(p):
    'tupindex : HASH math_expr tup'
    p[0] = p[3][p[2]]

def p_proposition_tup(p):
    'tup : LPAREN items RPAREN'
    p[0] = p[2]
    
def p_proposition_tupitems(p):
    'items : item'
    p[0] = [p[1]]
    
def p_proposition_tuptail(p):
    'items : items COMMA item'
    p[0] = p[1]
    p[0] += [p[3]]

def p_proposition_tupitem(p):
    '''
    item : str_expr
         | bool_expr
         | math_expr
    '''
    p[0] = p[1]

## Math functions

def p_proposition_setmath(p):
    'expr : math_expr'
    p[0] = p[1]

def p_proposition_number(p):
    '''
    math_expr : INTEGER
              | REAL
    '''
    p[0] = p[1]

def p_proposition_mathexpr(p):
    'math_expr : LPAREN math_expr RPAREN'
    p[0] = p[2]

def p_proposition_plus(p):
    'math_expr : math_expr PLUSOP math_expr'
    p[0] = p[1] + p[3]
    
def p_proposition_minus(p):
    'math_expr : math_expr MINUSOP math_expr'
    p[0] = p[1] - p[3]

def p_expression_uminus(p):
    'math_expr : MINUSOP math_expr %prec UMINUS'
    p[0] = -p[2]

def p_proposition_multiply(p):
    'math_expr : math_expr MULOP math_expr'
    p[0] = p[1] * p[3]

def p_proposition_divide(p):
    'math_expr : math_expr DIVOP math_expr'
    if p[3] == 0:
        raise ZeroDivisionError
    p[0] = p[1] / p[3]
    
def p_proposition_intdiv(p):
    'math_expr : math_expr INTDIVOP math_expr'
    if p[3] == 0:
        raise ZeroDivisionError
    p[0] = int(p[1] / p[3])

def p_proposition_mod(p):
    'math_expr : math_expr MODOP math_expr'
    p[0] = p[1] % p[3]
    
def p_proposition_exp(p):
    'math_expr : math_expr EXPOP math_expr'
    p[0] = pow(p[1], p[3])

## Boolean functions

def p_proposition_setbool(p):
    'expr : bool_expr'
    p[0] = p[1]

def p_proposition_bool(p):
    'bool_expr : BOOLEAN'
    p[0] = p[1]

def p_proposition_parenthetical(p):
    'bool_expr : LPAREN bool_expr RPAREN'
    p[0] = p[2]
    
def p_proposition_conjunction(p):
    'bool_expr : bool_expr CONJUNCTIONOP bool_expr'
    p[0] = True if p[1] and p[3] else False

def p_proposition_disjunction(p):
    'bool_expr : bool_expr DISJUNCTIONOP bool_expr'
    p[0] = True if p[1] or p[3] else False

def p_propsition_not(p):
    'bool_expr : NOTOP bool_expr' 
    p[0] = not p[2]
    
## String functions

def p_proposition_setstr(p):
    'expr : str_expr'
    p[0] = p[1]
    
def p_proposition_str(p):
    'str_expr : STRING'
    p[0] = p[1]
    
def p_proposition_strconcat(p):
    'str_expr : str_expr PLUSOP str_expr'
    p[0] = p[1] + p[3]
    
## String comparison    
   
def p_proposition_setcmp(p):   
    'expr : cmp_expr'
    p[0] = p[1]
    
def p_proposition_streq(p):
    'cmp_expr : str_expr EQOP str_expr'
    p[0] = p[1] == p[3]
    
def p_proposition_strneq(p):
    'cmp_expr : str_expr NEQOP str_expr'
    p[0] = p[1] != p[3]
    
def p_proposition_strlt(p):
    'cmp_expr : str_expr LTOP str_expr'
    p[0] = p[1] < p[3]

def p_proposition_strlte(p):
    'cmp_expr : str_expr LTEOP str_expr'
    p[0] = p[1] <= p[3]

def p_proposition_strgt(p):
    'cmp_expr : str_expr GTOP str_expr'
    p[0] = p[1] > p[3]

def p_proposition_strgte(p):
    'cmp_expr : str_expr GTEOP str_expr'
    p[0] = p[1] >= p[3]
    
## Math comparison

def p_proposition_numeq(p):
    'cmp_expr : math_expr EQOP math_expr'
    p[0] = p[1] == p[3]
    
def p_proposition_numneq(p):
    'cmp_expr : math_expr NEQOP math_expr'
    p[0] = p[1] != p[3]
    
def p_proposition_numlt(p):
    'cmp_expr : math_expr LTOP math_expr'
    p[0] = p[1] < p[3]

def p_proposition_numlte(p):
    'cmp_expr : math_expr LTEOP math_expr'
    p[0] = p[1] <= p[3]

def p_proposition_numgt(p):
    'cmp_expr : math_expr GTOP math_expr'
    p[0] = p[1] > p[3]

def p_proposition_numgte(p):
    'cmp_expr : math_expr GTEOP math_expr'
    p[0] = p[1] >= p[3]

## Parsing error

def p_error(p):
    print("SEMANTIC ERROR")
    print(f"p.value: {p.value}")
    sys.exit()

precedence = (
    ('left', 'DISJUNCTIONOP'),
    ('left', 'CONJUNCTIONOP'),
    ('left', 'NOTOP'),
    ('left', 'LTOP', 'GTOP', 'EQOP', 'LTEOP', 'GTEOP', 'NEQOP'),
    ('right', 'CONCATOP'),
    ('left', 'INOP'),
    ('left', 'PLUSOP', 'MINUSOP'),
    ('left', 'MULOP', 'DIVOP', 'INTDIVOP', 'MODOP'),
    ('right', 'EXPOP'),
    ('right','UMINUS'),
    ('left', 'COMMA'),
    ('left', 'LBRACKET', 'RBRACKET'),
    ('left', 'HASH'),
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
    print("RESULT: %s" % result)