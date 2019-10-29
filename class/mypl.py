import sys
import ply.lex as lex
import ply.yacc as yacc

# mypl.py
# Tokenizer, Parser, Evaluator for a simple propositional logic

# List of token names
tokens = (
          'VARIABLE',
          'NEGATION',
          'CONJUNCTION',
          'DISJUNCTION',
          'MATERIAL_IMPLICATION',
          'LPAREN',
          'RPAREN',
          )
          
t_NEGATION    = r'-'
t_CONJUNCTION = r'/\\'
t_DISJUNCTION = r'\\/'
t_MATERIAL_IMPLICATION = r'-->'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'

def t_VARIABLE(t):
    r'[a-z]\d{0,2}'
    t.value = t.value
    return t
    
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_error(t):
    print("SYNTAX ERROR: %s at %d" % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)
    
lexer = lex.lex()

#prop = input("Enter a proposition: ")

#lexer.input(prop)
#for tok in lexer:
#    print(tok.type, tok.value, tok.lineno, tok.lexpos)

#sys.exit()

# GRAMMAR FOR PARSING

def p_proposition_negation(p):
    'proposition : NEGATION proposition'

def p_proposition_conjunction(p):
    'proposition : proposition CONJUNCTION proposition'

def p_proposition_disjunction(p):
    'proposition : proposition DISJUNCTION proposition'

def p_proposition_material_implication(p):
    'proposition : proposition MATERIAL_IMPLICATION proposition'

def p_proposition_parenthetical(p):
    'proposition : LPAREN proposition RPAREN'
        
def p_proposition_var(p):
    'proposition : VARIABLE'

def p_error(p):
    print("SYNTAX ERROR")
    
# Manually setting precedence and associativity to resolve ambiguity in the
# grammar.    
precedence = (
              ('right', 'MATERIAL_IMPLICATION'),
              ('left', 'DISJUNCTION'),
              ('left', 'CONJUNCTION'),
              ('right', 'NEGATION'),
              )
    
parser = yacc.yacc()

while True:
    try:
        s = input("Enter a proposition: ")
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print("RESULT:", result)