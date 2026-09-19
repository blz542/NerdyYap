from nerdyap.token import Token, TokenType


class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def advance(self):
        char = self.source[self.position]

        self.position += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char

    def tokenize(self):
        tokens = []

        while self.position < len(self.source):
            current = self.source[self.position]

            if current.isspace():
                self.advance()
                continue

            line = self.line
            column = self.column

            if current.isdigit():
                tokens.append(self.read_number(line, column))
                continue

            if current.isalpha() or current == "_":
                tokens.append(self.read_identifier(line, column))
                continue

            if current == '"':
                tokens.append(self.read_string(line, column))
                continue

            single_char_tokens = {
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.STAR,
                "/": TokenType.SLASH,

                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                
                "{": TokenType.LBRACE,
                "}": TokenType.RBRACE,

                ";": TokenType.SEMICOLON,
            }

            if current in single_char_tokens:
                token_type = single_char_tokens[current]

                self.advance()

                tokens.append(
                    Token(token_type, current, line, column)
                )

                continue

            raise SyntaxError(
                f"skill issue at ln {line}, col {column}"
            )

        tokens.append(
            Token(TokenType.EOF, None, self.line, self.column)
        )

        return tokens

    def read_number(self, line, column):
        start = self.position

        while (
            self.position < len(self.source)
            and self.source[self.position].isdigit()
        ):
            self.advance()

        value = self.source[start:self.position]

        return Token(
            TokenType.NUMBER,
            int(value),
            line,
            column
        )

    def read_identifier(self, line, column):
        start = self.position

        while (
            self.position < len(self.source)
            and (
                self.source[self.position].isalnum()
                or self.source[self.position] == "_"
            )
        ):
            self.advance()

        value = self.source[start:self.position]

        keywords = {
            "yo": TokenType.YO,
            "be": TokenType.BE,
            "yap": TokenType.YAP,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "mogs": TokenType.MOGS,
            "gets": TokenType.GETS,
            "mogged": TokenType.MOGGED,
            "by": TokenType.BY,
            "larping": TokenType.LARPING,
        }

        token_type = keywords.get(
            value,
            TokenType.IDENTIFIER
        )

        return Token(
            token_type,
            value,
            line,
            column
        )

    def read_string(self, line, column):
        self.advance()  # opening "

        start = self.position

        while (
            self.position < len(self.source)
            and self.source[self.position] != '"'
        ):
            self.advance()

        if self.position >= len(self.source):
            raise SyntaxError(
                f"skill issue at ln {line}, col {column}"
            )

        value = self.source[start:self.position]

        self.advance()  # closing "

        return Token(
            TokenType.STRING,
            value,
            line,
            column
        )