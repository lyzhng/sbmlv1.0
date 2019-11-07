# Code written by Lily Zhong

import sys
import ply.lex as lex
import ply.yacc as yacc
from sys import argv

## Exceptions

class SemanticError(RuntimeError):
    def __init__(self):
        super(SemanticError, self).__init__("SEMANTIC ERROR")

class SyntaxError(Exception):
    def __init__(self):
        super(SyntaxError, self).__init__("SYNTAX ERROR")
        

# DEBUG = len(sys.argv) > 1 and sys.argv[1] == "--debug"

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
    r'(([-]?([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+))([eE][-]?[0-9]+)?)'
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
    raise SyntaxError
    
lexer = lex.lex()

## PARSING
    
## Start statement    
    
def p_expr(p):
    'stmt : expr SEMICOLON'
    p[0] = p[1]    
    
def p_paren(p):
    '''
    expr : LPAREN expr RPAREN
    '''
    p[0] = p[2]      
    
## Wherever expr leads to... terminals and nested expressions 
    
def p_term(p):
    '''
    expr : STRING
         | INTEGER
         | REAL
         | BOOLEAN
         | list
         | tup
         | listindex
         | tupindex
    '''
    p[0] = p[1]
          
## Unary operations       
           
def p_not(p):
    'expr : NOTOP expr'
    p[0] = not p[2] 
       
def p_uminus(p):
    'expr : MINUSOP expr %prec UMINUS'
    p[0] = -p[2]       
       
## Binary operations       
       
def p_binop(p):
    '''
    expr : expr PLUSOP expr
         | expr MINUSOP expr
         | expr MULOP expr
         | expr DIVOP expr
         | expr INTDIVOP expr
         | expr MODOP expr
         | expr EXPOP expr
         | expr CONJUNCTIONOP expr
         | expr DISJUNCTIONOP expr
         | expr INOP expr
         | expr CONSOP expr
    '''
    if p[2] == '+':
        both_numbers = _valid_types([p[1], p[3]], [int, float])
        both_strings = _valid_types([p[1], p[3]], [str])
        both_lists = _valid_types([p[1], p[3]], [list])
        if both_numbers or both_strings or both_lists:
            p[0] = p[1] + p[3]
            return
    elif p[2] == '-':
        if _valid_types([p[1], p[3]], [int, float]):
            p[0] = p[1] - p[3]
            return
    elif p[2] == '*':
        if _valid_types([p[1], p[3]], [int, float]):
            p[0] = p[1] * p[3]
            return
    elif p[2] == '/':
        if p[3] == 0:
            raise SemanticError
        if _valid_types([p[1], p[3]], [int, float]):
            p[0] = p[1] / p[3]
            return
    elif p[2] == 'div':
        if _valid_types([p[1], p[3]], [int]):
            if p[3] == 0:
                raise SemanticError
            p[0] = p[1] // p[3]
            return
    elif p[2] == 'mod':
        if _valid_types([p[1], p[3]], [int]):
            p[0] = p[1] % p[3]
            return
    elif p[2] == '**':
        if _valid_types([p[1], p[3]], [int, float]):
            p[0] = pow(p[1], p[3])  
            return  
    elif p[2] == 'andalso':
        if _valid_types([p[1], p[3]], [bool]):
            p[0] = p[1] and p[3]
            return
    elif p[2] == 'orelse':
        if _valid_types([p[1], p[3]], [bool]):
            p[0] = p[1] or p[3]
            return
    elif p[2] == 'in':
        if (_valid_types([p[1]], [int, float, bool, str, list, tuple]) and _valid_types([p[3]], [list])) or _valid_types([p[1], p[3]], [str]):
            p[0] = p[1] in p[3]
            return
    elif p[2] == '::':
        if _valid_types([p[1]], [int, float, bool, str, list, tuple]) and _valid_types([p[3]], [list]):
            p[0] = [p[1]] + p[3]
            return
    raise SemanticError       
       
def p_comparison(p):
    '''
    expr : expr EQOP expr
         | expr NEQOP expr
         | expr GTOP expr
         | expr GTEOP expr
         | expr LTOP expr
         | expr LTEOP expr
    '''        
    if _valid_types([p[1], p[3]], [int, float]) or _valid_types([p[1], p[3]], [str]):
        if p[2] == '==':
            p[0] = p[1] == p[3]
        elif p[2] == '<>':
            p[0] = p[1] != p[3]
        elif p[2] == '>':
            p[0] = p[1] > p[3]
        elif p[2] == '>=':
            p[0] = p[1] >= p[3]
        elif p[2] == '<':
            p[0] = p[1] < p[3]
        elif p[2] == '<=':
            p[0] = p[1] <= p[3]                           
        return
    raise SemanticError

## Lists

def p_list(p):
    '''
    list : LBRACKET listitems RBRACKET
         | LBRACKET RBRACKET
    '''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = [] 
        
def p_listitems(p):
    '''
    listitems : listitems COMMA listitem
              | listitem
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]   

def p_listitem(p):
    'listitem : expr'
    p[0] = [p[1]]

def p_genindex(p):
    '''
    listindex : list LBRACKET expr RBRACKET
              | expr LBRACKET expr RBRACKET
    '''
    is_int_index = type(p[3]) == int
    if is_int_index and p[3] < 0 or p[3] >= len(p[1]): 
        raise SemanticError
    if _valid_types([p[3]], [int]) and _valid_types([p[1]], [list, str]):
        p[0] = p[1][p[3]]
        return
    raise SemanticError
    
## Tuples    
    
def p_tuple(p):
    '''
    tup : LPAREN tupitems RPAREN
        | LPAREN RPAREN
    '''
    if len(p) == 3:
        p[0] = ()
    elif len(p) == 4:
        p[0] = tuple(p[2])
    elif len(p[2]) == 1:
        p[0] = p[2][0]
                
def p_tupitems(p):
    '''
    tupitems : tupitems COMMA tupitem
             | tupitems COMMA
             | tupitem
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]                
                
def p_tupitem(p):
    'tupitem : expr'
    p[0] = [p[1]]
    
def p_tupindex(p):
    '''
    tupindex : HASH INTEGER LPAREN tupindex RPAREN
             | HASH INTEGER tup
    '''
    if len(p) == 6:
        if p[2] <= 0 or p[2] > len(p[4]):
            raise SemanticError
        p[0] = p[4][p[2]-1]
    else:
        if p[2] <= 0 or p[2] > len(p[3]):
            raise SemanticError
        p[0] = p[3][p[2]-1]

def _valid_types(arguments, types):
    """
    Check if all the arguments are in the types list
    """
    for arg in arguments:
        if type(arg) not in types:
            return False
    return True

## Parsing error

def p_error(p):
    raise SemanticError

## Precedence

precedence = (
    ('left', 'DISJUNCTIONOP'),
    ('left', 'CONJUNCTIONOP'),
    ('left', 'NOTOP'),
    ('left', 'LTOP', 'LTEOP', 'EQOP', 'NEQOP', 'GTEOP', 'GTOP'),
    ('right', 'CONSOP'),
    ('left', 'INOP'),
    ('left', 'PLUSOP', 'MINUSOP'),
    ('left', 'MULOP', 'DIVOP', 'INTDIVOP', 'MODOP'),
    ('right', 'EXPOP'),
    ('right','UMINUS'),
    ('left', 'LBRACKET', 'RBRACKET'),
    ('left', 'HASH'),
    ('left', 'COMMA'),
    ('left', 'LPAREN', 'RPAREN'),
)

parser = yacc.yacc()

# FOR DEBUGGING PURPOSES
# while True:
#     try:
#         s = input("Enter a proposition: ")
#     except EOFError:
#         break
#     if not s:
#         continue
#     result = parser.parse(s, debug=True)
#     print(f"RESULT: {result}")

# FOR SUBMISSION
with open(argv[1], 'r') as file:
    for line in file:
        try:
            result = parser.parse(line, debug=False)
            print(result)
        except EOFError:
            break
        except Exception as err:
            print(err)
            continue