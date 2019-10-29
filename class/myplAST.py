import ply.lex as lex
import ply.yacc as yacc

# mypl AST

# Global
indent_level = 0

def print_alot(p):
    print("P:", p)
    print("DIR:", dir(p))
    print("SLICE", p.slice)
    print("STACK", p.stack)

class Node():
    def __init__(self, parent = None, lineno = 0, colno = 0):
        self.parent = parent
        self.lineno = lineno
        self.colno = colno

class Variable(Node):
    def __init__(self, parent = None, lineno = 0, colno = 0, name = ""):
        super().__init__(parent, lineno, colno)
        self.name = name
        
    def __str__(self):
        return "Variable: " +  self.name

class Negation(Node):
    def __init__(self, parent = None, lineno = 0, colno = 0, subprop = None):
        super().__init__(parent, lineno, colno)
        self.subprop = subprop
        
    def __str__(self):
        res = "Negation:"
        global indent_level
        indent_level += 1
        res += "\n" + ("  " * indent_level) + "Child: " + str(self.subprop)
        indent_level -= 1
        return res
        
class Conjunction(Node):
    def __init__(self, parent = None, lineno = 0, colno = 0, left = None, right = None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right
        
    def __str__(self):
        res = "Conjunction:"
        global indent_level
        indent_level += 1
        res += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        res += "\n" + ("  " * indent_level) + "Right: " + str(self.right)
        indent_level -= 1
        return res
        
class Disjunction(Node):
    def __init__(self, parent = None, lineno = 0, colno = 0, left = None, right = None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right
        
    def __str__(self):
        res = "Disjunction:"
        global indent_level
        indent_level += 1
        res += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        res += "\n" + ("  " * indent_level) + "Right: " + str(self.right)
        indent_level -= 1
        return res

class Material_Implication(Node):
    def __init__(self, parent = None, lineno = 0, colno = 0, left = None, right = None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right
        
    def __str__(self):
        res = "Material Implication:"
        global indent_level
        indent_level += 1
        res += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        res += "\n" + ("  " * indent_level) + "Right: " + str(self.right)
        indent_level -= 1
        return res


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
    p[0] = Negation(None, p.lineno, p.lexpos, p[2])
    p[2].parent = p[0]
    #print_alot(p)
    #for x in p.slice:
    #    print("S:", x, ":", type(x), "--", x.value)
    
def p_proposition_conjunction(p):
    'proposition : proposition CONJUNCTION proposition'
    p[0] = Conjunction(None, p.lineno, p.lexpos, p[1], p[3])
    p[1].parent = p[0]
    p[3].parent = p[0]
    #print_alot(p)
    #for x in p.slice:
    #    print("S:", x, ":", type(x), "--", x.value)
    
def p_proposition_disjunction(p):
    'proposition : proposition DISJUNCTION proposition'
    p[0] = Disjunction(None, p.lineno, p.lexpos, p[1], p[3])
    p[1].parent = p[0]
    p[3].parent = p[0]
    #print_alot(p)
    #for x in p.slice:
    #    print("S:", x, ":", type(x), "--", x.value)
    
def p_proposition_material_implication(p):
    'proposition : proposition MATERIAL_IMPLICATION proposition'
    p[0] = Material_Implication(None, p.lineno, p.lexpos, p[1], p[3])
    p[1].parent = p[0]
    p[3].parent = p[0]
    #print_alot(p)
    #for x in p.slice:
    #    print("S:", x, ":", type(x), "--", x.value)
    
def p_proposition_parenthetical(p):
    'proposition : LPAREN proposition RPAREN'
    p[0] = p[2]
    #print_alot(p)
    #for x in p.slice:
    #    print("S:", x, ":", type(x), "--", x.value)
    
def p_proposition_var(p):
    'proposition : VARIABLE'
    p[0] = Variable(None, p.lineno, p.lexpos, p[1])
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

try:
    s = input("Enter a proposition: ")
except EOFError as e:
    print(e)
result = parser.parse(s)#, debug = True)
print(result)

#while True:
#    try:
#        s = input("Enter a proposition: ")
#    except EOFError:
#        break
#    if not s:
#        continue
#    result = parser.parse(s)#, debug = True)
#    print(result)