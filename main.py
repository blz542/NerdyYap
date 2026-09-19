import sys

from nerdyap.lexer import Lexer
from nerdyap.parser import Parser
from nerdyap.interpreter import Interpreter


if len(sys.argv) != 2:
    print("skill issue: give me a .nerd file")
    sys.exit(1)


filename = sys.argv[1]

with open(filename, "r", encoding="utf-8") as file:
    source = file.read()


lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
statements = parser.parse()

interpreter = Interpreter()
interpreter.run(statements)