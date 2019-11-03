# Code written by Lily Zhong

import sys
import ply.lex as lex
import ply.yacc as yacc
from exceptions import SemanticError, SyntaxError
from sys import argv

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
    'CONSOP',
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
t_CONSOP = r'\:{2}'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_HASH = r'\#'

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

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

## Lexing error

def t_error(t):
    t.lexer.skip(1)
    raise SyntaxError()

lexer = lex.lex()

## PARSING

## General

def p_proposition_expr(p):
    'stmt : expr SEMICOLON'
    p[0] = p[1]

def p_proposition_add(p):
    'list : list PLUSOP list'
    if type(p[1]) != type(p[3]):
        raise SemanticError()
    p[0] = p[1] + p[3]

## List functions

def p_proposition_setter(p):
    '''
    expr : list
         | cmp_expr
         | bool_expr
         | math_expr
         | str_expr
         | tupindex
    '''
    p[0] = p[1]

def p_proposition_index(p):
    '''
    listindex : str_expr listindextail
              | list listindextail
    '''
    if type(p[2]) != int:
        raise SemanticError()
    p[0] = p[1][p[2]]

def p_proposition_indextail(p):
    '''
    listindextail : LBRACKET math_expr RBRACKET
    '''
    if type(p[2]) != int:
        raise SemanticError()
    p[0] = p[2]


def p_proposition_list(p):
    '''
    list : LBRACKET items RBRACKET
         | listindex
         | LBRACKET RBRACKET
    '''
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        p[0] = [];
    else:
        p[0] = p[1]
    
def p_proposition_cons(p):
    '''
    expr : list CONSOP list
         | math_expr CONSOP list
         | str_expr CONSOP list
         | bool_expr CONSOP list
    '''
    p[0] = [p[1]] + p[3]
    
def p_proposition_in(p):
    '''
    cmp_expr : str_expr INOP str_expr
             | item INOP list
    '''
    p[0] = p[1] in p[3]

    
## Tuple functions

def p_proposition_tupindex(p):
    '''
    tupindex : HASH INTEGER LPAREN tupindex RPAREN
             | HASH INTEGER tup
    '''
    if len(p) > 4:
        if p[2] > len(p[4]) or p[2] <= 0:
            raise SemanticError()
        p[0] = p[4][p[2]-1]
    else: 
        p[0] = p[3][p[2]-1]

def p_proposition_tup(p):
    '''
    tup : LPAREN items RPAREN
    '''
    
    p[0] = tuple(p[2])
    
def p_proposition_tuptail(p):
    '''
    items : item COMMA items
          | item COMMA 
          | item
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_proposition_tupitem(p):
    '''
    item : bool_expr
         | math_expr
         | tup
         | str_expr
         | list
    '''
    p[0] = p[1]


## Math functions

def p_proposition_setnum(p):
    '''
    math_expr : INTEGER
              | REAL
    '''
    p[0] = p[1]

def p_proposition_mathparen(p):
    'math_expr : LPAREN math_expr RPAREN'
    p[0] = p[2]

def p_proposition_mathplus(p):
    'math_expr : math_expr PLUSOP math_expr'
    p[0] = p[1] + p[3]
        
def p_proposition_mathminus(p):
    'math_expr : math_expr MINUSOP math_expr'
    if type(p[1]) != type(p[3]):
        raise SemanticError()
    p[0] = p[1] - p[3]

def p_proposition_uminus(p):
    'math_expr : MINUSOP math_expr %prec UMINUS'
    p[0] = -p[2]

def p_proposition_mathmul(p):
    'math_expr : math_expr MULOP math_expr'
    if type(p[1]) != type(p[3]):
        raise SemanticError()
    p[0] = p[1] * p[3]
    
def p_proposition_mathdiv(p):
    'math_expr : math_expr DIVOP math_expr'
    if type(p[1]) != float and type(p[3]) != float:
        raise SemanticError()
    if p[3] == 0:
        raise ZeroDivisionError
    p[0] = p[1] / p[3]

def p_proposition_intdiv(p):
    'math_expr : math_expr INTDIVOP math_expr'
    if type(p[1]) != int and type(p[3]) != int:
        raise SemanticError()
    if p[3] == 0:
        raise ZeroDivisionError
    p[0] = int(p[1] / p[3])

def p_proposition_mod(p):
    'math_expr : math_expr MODOP math_expr'
    if type(p[1]) != int and type(p[3]) != int:
        raise SemanticError()
    p[0] = p[1] % p[3]
    
def p_proposition_exp(p):
    'math_expr : math_expr EXPOP math_expr'
    p[0] = pow(p[1], p[3])


## Boolean functions

def p_proposition_bool(p):
    'bool_expr : BOOLEAN'
    p[0] = p[1]

def p_proposition_parenthetical(p):
    'bool_expr : LPAREN bool_expr RPAREN'
    p[0] = p[2]
    
def p_proposition_conjunction(p):
    'bool_expr : bool_expr CONJUNCTIONOP bool_expr'
    p[0] = p[1] and p[3]

def p_proposition_disjunction(p):
    'bool_expr : bool_expr DISJUNCTIONOP bool_expr'
    p[0] = p[1] or p[3]

def p_propsition_not(p):
    '''
    bool_expr : NOTOP bool_expr
              | NOTOP cmp_expr
    ''' 
    p[0] = not p[2]
    
    
## String functions

def p_proposition_str(p):
    'str_expr : STRING'
    p[0] = p[1]
    
def p_proposition_strconcat(p):
    'str_expr : str_expr PLUSOP str_expr'
    p[0] = p[1] + p[3]
    
## String comparison    
    
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
    # raise SemanticError()
    print("SEMANTIC ERROR")
    sys.exit()

precedence = (
    ('left', 'DISJUNCTIONOP'),
    ('left', 'CONJUNCTIONOP'),
    ('left', 'NOTOP'),
    ('left', 'LTOP', 'GTOP', 'EQOP', 'LTEOP', 'GTEOP', 'NEQOP'),
    ('right', 'CONSOP'),
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
    print(f"RESULT: {result}")

# with open(argv[1], 'r') as file:
#     for line in file:
#         try:
#             result = parser.parse(line, debug=False)
#             print(result)
#         except EOFError:
#             break
#         except (SemanticError, SyntaxError) as err:
#             print(err)
#             continue