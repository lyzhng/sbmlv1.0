import ply.lex as lex
import ply.yacc as yacc

def print_alot(p):
    print("P:", p)
    print("DIR:", dir(p))
    print("SLICE", p.slice)
    print("STACK", p.stack)

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

# GRAMMAR FOR PARSING

def p_proposition_negation(p):
    'proposition : NEGATION proposition'
    p[0] = "not " + p[2]
    #print("NEGATION:", p)
    #for x in p:
    #    print(x)
    #print_alot(p)
    #for x in p.slice:
    #    print("S:", x, ":", type(x), "--", x.value)

def p_proposition_conjunction(p):
    'proposition : proposition CONJUNCTION proposition'
    p[0] = p[1] + " and " + p[3]
    #print("CONJUNCTION:", p)
    #for x in p:
    #    print(x)
    #print_alot(p)
    #for x in p.slice:
    #    print("S:", x, ":", type(x), "--", x.value)

def p_proposition_disjunction(p):
    'proposition : proposition DISJUNCTION proposition'
    p[0] = p[1] + " or " + p[3]
    #print("DISJUNCTION:", p)
    #for x in p:
    #    print(x)
    #print_alot(p)
    #for x in p.slice:
    #    print("S:", x, ":", type(x), "--", x.value)

def p_proposition_material_implication(p):
    'proposition : proposition MATERIAL_IMPLICATION proposition'
    p[0] = "if " + p[1] + " then " + p[3]
    #print("MATERIAL_IMPLCIATION:", p)
    #for x in p:
    #    print(x)
    #print_alot(p)
    #for x in p.slice:
    #    print("S:", x, ":", type(x), "--", x.value)

def p_proposition_parenthetical(p):
    'proposition : LPAREN proposition RPAREN'
    p[0] = p[2]
    #print("PARENTHETICAL:", p)
    #for x in p:
    #    print(x)
    #print_alot(p)
    #for x in p.slice:
    #    print("S:", x, ":", type(x), "--", x.value)

def p_proposition_var(p):
    'proposition : VARIABLE'
    p[0] = p[1]
    #print("VARIABLE:", p)
    #for x in p:
    #    print(x)
    #print_alot(p)
    #for x in p.slice:
    #    print("S:", x, ":", type(x), "--", x.value)

def p_error(p):
    print("SYNTAX ERROR")


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
    result = parser.parse(s)#, debug = True)
    print("RESULT:", result)
