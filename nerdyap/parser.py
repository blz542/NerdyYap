from nerdyap.token import TokenType

class Parser:
    def __init__(self, tokens): self.tokens, self.position = tokens, 0
    def current(self): return self.tokens[self.position]
    def advance(self): token=self.current(); self.position+=1; return token
    def error(self):
        t=self.current(); raise SyntaxError(f"skill issue at ln {t.line}, col {t.column}")
    def missing_semicolon(self):
        t=self.tokens[self.position-1]; col=t.column if t.value is None else t.column+len(str(t.value))
        raise SyntaxError(f"really bruh??? check ln {t.line}, col {col}")
    def parse(self): return self.statements(TokenType.EOF)
    def statements(self, end):
        out=[]
        while self.current().type != end:
            if self.current().type == TokenType.EOF: self.error()
            s=self.statement(); out.append(s)
            if s["type"] not in ("if","while","for","do_while"):
                if self.current().type != TokenType.SEMICOLON: self.missing_semicolon()
                self.advance()
        if end != TokenType.EOF: self.advance()
        return out
    def statement(self):
        t=self.current().type
        if t==TokenType.YO: return self.variable()
        if t==TokenType.YAP: self.advance(); return {"type":"yap","value":self.expression()}
        if t==TokenType.IF: return self.if_stmt()
        if t==TokenType.WHILE: return self.loop("while")
        if t==TokenType.GRIND: return self.do_while()
        if t==TokenType.FOR: return self.for_stmt()
        if t in (TokenType.BREAK,TokenType.CONTINUE): self.advance(); return {"type":t.name.lower()}
        self.error()
    def variable(self):
        self.advance(); n=self.advance()
        if n.type!=TokenType.IDENTIFIER: self.error()
        if self.current().type==TokenType.LBRACKET:
            target=self.index({"type":"value","value":n.value})
            if self.advance().type!=TokenType.BE: self.error()
            return {"type":"assignment","target":target,"value":self.expression()}
        if self.advance().type!=TokenType.BE: self.error()
        return {"type":"variable","name":n.value,"value":self.expression()}
    def block(self):
        if self.current().type!=TokenType.LBRACE: self.error()
        self.advance(); return self.statements(TokenType.RBRACE)
    def if_stmt(self):
        self.advance(); c=self.condition(); body=self.block(); other=None
        if self.current().type==TokenType.ELSE: self.advance(); other=self.block()
        return {"type":"if","condition":c,"if_statements":body,"else_statements":other}
    def loop(self, kind):
        self.advance(); return {"type":kind,"condition":self.condition(),"statements":self.block()}
    def do_while(self):
        self.advance(); body=self.block()
        if self.current().type!=TokenType.WHILE: self.error()
        self.advance(); c=self.condition()
        if self.current().type!=TokenType.SEMICOLON: self.missing_semicolon()
        self.advance(); return {"type":"do_while","condition":c,"statements":body}
    def for_stmt(self):
        self.advance(); n=self.advance()
        if n.type!=TokenType.IDENTIFIER or self.advance().type!=TokenType.IN: self.error()
        return {"type":"for","name":n.value,"iterable":self.expression(),"statements":self.block()}
    def assignment(self):
        if self.tokens[self.position+1].type==TokenType.BE:
            target={"type":"variable_target","name":self.advance().value}
        else:
            target=self.index()
        if self.advance().type!=TokenType.BE: self.error()
        return {"type":"assignment","target":target,"value":self.expression()}
    def condition(self):
        left=self.expression(); t=self.current().type
        if t==TokenType.MOGS: op="mogs"; self.advance()
        elif t==TokenType.LARPING: op="larping"; self.advance()
        elif t==TokenType.GETS:
            self.advance()
            if self.advance().type!=TokenType.MOGGED or self.advance().type!=TokenType.BY: self.error()
            op="mogged_by"
        else: self.error()
        return {"left":left,"operator":op,"right":self.expression()}
    def expression(self):
        x=self.term()
        while self.current().type in (TokenType.PLUS,TokenType.MINUS):
            o=self.advance(); x={"type":"binary","left":x,"operator":o.value,"right":self.term()}
        return x
    def term(self):
        x=self.value()
        while self.current().type in (TokenType.STAR,TokenType.SLASH):
            o=self.advance(); x={"type":"binary","left":x,"operator":o.value,"right":self.value()}
        return x
    def value(self):
        if self.current().type==TokenType.LPAREN:
            self.advance(); x=self.expression()
            if self.current().type!=TokenType.RPAREN: self.error()
            self.advance(); return x
        if self.current().type==TokenType.LBRACKET: return self.array()
        t=self.advance()
        if t.type not in (TokenType.NUMBER,TokenType.STRING,TokenType.CHAR,TokenType.IDENTIFIER): self.error()
        x={"type":"value","value":t.value}
        return self.index(x) if t.type==TokenType.IDENTIFIER and self.current().type==TokenType.LBRACKET else x
    def index(self, base=None):
        if base is None:
            t=self.advance()
            if t.type!=TokenType.IDENTIFIER: self.error()
            base={"type":"value","value":t.value}
        return self.index_from(base)
    def index_from(self, base):
        self.advance(); i=self.expression()
        if self.current().type!=TokenType.RBRACKET: self.error()
        self.advance(); return {"type":"index","array":base,"index":i}
    def array(self):
        self.advance(); values=[]
        while self.current().type!=TokenType.RBRACKET:
            values.append(self.expression())
            if self.current().type!=TokenType.COMMA: break
            self.advance()
        if self.current().type!=TokenType.RBRACKET: self.error()
        self.advance(); return {"type":"array","values":values}
