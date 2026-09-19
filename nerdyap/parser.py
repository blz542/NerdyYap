from nerdyap.token import TokenType


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current()
        self.position += 1
        return token

    def error(self):
        token = self.current()

        raise SyntaxError(
            f"skill issue at ln {token.line}, col {token.column}"
        )

    def missing_semicolon(self):
        token = self.tokens[self.position - 1]

        if token.value is None:
            column = token.column
        else:
            column = token.column + len(str(token.value))

        raise SyntaxError(
            f"really bruh??? check ln {token.line}, col {column}"
        )

    def parse(self):
        statements = []

        while self.current().type != TokenType.EOF:
            statement = self.parse_statement()
            statements.append(statement)

            if statement["type"] == "if":
                continue

            if self.current().type != TokenType.SEMICOLON:
                self.missing_semicolon()

            self.advance()

        return statements

    def parse_statement(self):
        token = self.current()

        if token.type == TokenType.YO:
            return self.parse_variable()

        if token.type == TokenType.YAP:
            return self.parse_yap()

        if token.type == TokenType.IF:
            return self.parse_if()

        self.error()

    def parse_variable(self):
        self.advance()  # yo

        name = self.advance()

        if name.type != TokenType.IDENTIFIER:
            self.error()

        be = self.advance()

        if be.type != TokenType.BE:
            self.error()

        value = self.parse_expression()

        return {
            "type": "variable",
            "name": name.value,
            "value": value
        }

    def parse_yap(self):
        self.advance()  # yap

        value = self.parse_expression()

        return {
            "type": "yap",
            "value": value
        }

    def parse_if(self):
        self.advance()  # if

        condition = self.parse_condition()

        if self.current().type != TokenType.LBRACE:
            self.error()

        self.advance()  # {

        if_statements = []

        while self.current().type != TokenType.RBRACE:
            if self.current().type == TokenType.EOF:
                self.error()

            statement = self.parse_statement()
            if_statements.append(statement)

            if statement["type"] == "if":
                continue

            if self.current().type != TokenType.SEMICOLON:
                self.missing_semicolon()

            self.advance()

        self.advance()  # }

        else_statements = None

        if self.current().type == TokenType.ELSE:
            self.advance()  # else

            if self.current().type != TokenType.LBRACE:
                self.error()

            self.advance()  # {

            else_statements = []

            while self.current().type != TokenType.RBRACE:
                if self.current().type == TokenType.EOF:
                    self.error()

                statement = self.parse_statement()
                else_statements.append(statement)

                if statement["type"] == "if":
                    continue

                if self.current().type != TokenType.SEMICOLON:
                    self.missing_semicolon()

                self.advance()

            self.advance()  # }

        return {
            "type": "if",
            "condition": condition,
            "if_statements": if_statements,
            "else_statements": else_statements
        }

    def parse_condition(self):
        left = self.parse_expression()

        operator = self.current()

        if operator.type == TokenType.MOGS:
            self.advance()

            right = self.parse_expression()

            return {
                "type": "condition",
                "left": left,
                "operator": "mogs",
                "right": right
            }

        if operator.type == TokenType.LARPING:
            self.advance()

            right = self.parse_expression()

            return {
                "type": "condition",
                "left": left,
                "operator": "larping",
                "right": right
            }

        if operator.type == TokenType.GETS:
            self.advance()  # gets

            if self.current().type != TokenType.MOGGED:
                self.error()

            self.advance()  # mogged

            if self.current().type != TokenType.BY:
                self.error()

            self.advance()  # by

            right = self.parse_expression()

            return {
                "type": "condition",
                "left": left,
                "operator": "mogged_by",
                "right": right
            }

        self.error()

    def parse_expression(self):
        left = self.parse_term()

        while self.current().type in (
            TokenType.PLUS,
            TokenType.MINUS
        ):
            operator = self.advance()
            right = self.parse_term()

            left = {
                "type": "binary",
                "left": left,
                "operator": operator.value,
                "right": right
            }

        return left

    def parse_term(self):
        left = self.parse_value()

        while self.current().type in (
            TokenType.STAR,
            TokenType.SLASH
        ):
            operator = self.advance()
            right = self.parse_value()

            left = {
                "type": "binary",
                "left": left,
                "operator": operator.value,
                "right": right
            }

        return left

    def parse_value(self):
        token = self.current()

        if token.type == TokenType.LPAREN:
            self.advance()

            expression = self.parse_expression()

            if self.current().type != TokenType.RPAREN:
                self.error()

            self.advance()

            return expression

        token = self.advance()

        if token.type not in (
            TokenType.NUMBER,
            TokenType.STRING,
            TokenType.IDENTIFIER
        ):
            self.error()

        return {
            "type": "value",
            "value": token.value
        }