from enum import Enum


class TokenType(Enum):
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"

    YO = "YO"
    BE = "BE"
    YAP = "YAP"
    IF = "IF"
    ELSE = "ELSE"

    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"

    MOGS = "MOGS"
    GETS = "GETS"
    MOGGED = "MOGGED"
    BY = "BY"
    LARPING = "LARPING"

    LPAREN = "LPAREN"
    RPAREN = "RPAREN"

    LBRACE = "LBRACE"
    RBRACE = "RBRACE"

    SEMICOLON = "SEMICOLON"

    EOF = "EOF"


class Token:
    def __init__(self, type, value, line=1, column=1):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return (
            f"Token({self.type.name}, {self.value!r}, "
            f"ln {self.line}, col {self.column})"
        )