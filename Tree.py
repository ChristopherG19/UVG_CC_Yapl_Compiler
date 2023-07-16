from antlr4 import *
from YALPParser import YALPParser
from YALPLexer import YALPLexer

def beautify_lisp_string(in_string):
   indent_size = 4
   add_indent = ' '*indent_size
   out_string = in_string[0]
   indent = ''
   for i in range(1, len(in_string)):
       if in_string[i] == '(' and in_string[i+1] != ' ':
           indent += add_indent
           out_string += '\n' + indent + '(' 
       elif in_string[i] == ')':
           out_string += ')'
           if len(indent) > 0:
               indent = indent.replace(add_indent, '', 1)
       else:
           out_string += in_string[i]
   return out_string

file_name = 'test1.expr'
input_stream = FileStream(file_name)
lexer = YALPLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = YALPParser(token_stream)
tree = parser.prog()

print('Tree:')
lisp_tree_str = tree.toStringTree(recog=parser)
print(beautify_lisp_string(lisp_tree_str))
print()
