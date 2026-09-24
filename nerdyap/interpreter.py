class _Break(Exception): pass
class _Continue(Exception): pass

class Interpreter:
    def __init__(self): self.variables={}
    def run(self, statements):
        for s in statements: self.execute(s)
    def execute(self,s):
        k=s["type"]
        if k=="variable": self.variables[s["name"]]=self.evaluate(s["value"])
        elif k=="assignment":
            t=s["target"]
            if t["type"]=="variable_target": self.variables[t["name"]]=self.evaluate(s["value"])
            else: self.evaluate(t["array"])[self.evaluate(t["index"])] = self.evaluate(s["value"])
        elif k=="yap": print(self.evaluate(s["value"]))
        elif k=="if": self.run(s["if_statements"] if self.condition(s["condition"]) else (s["else_statements"] or []))
        elif k=="while":
            while self.condition(s["condition"]):
                try: self.run(s["statements"])
                except _Continue: continue
                except _Break: break
        elif k=="do_while":
            while True:
                try: self.run(s["statements"])
                except _Break: break
                except _Continue: pass
                if not self.condition(s["condition"]): break
        elif k=="for":
            for value in self.evaluate(s["iterable"]):
                self.variables[s["name"]]=value
                try: self.run(s["statements"])
                except _Continue: continue
                except _Break: break
        elif k=="break": raise _Break()
        elif k=="continue": raise _Continue()
    def evaluate(self,e):
        if e["type"]=="value": return self.variables.get(e["value"],e["value"])
        if e["type"]=="array": return [self.evaluate(x) for x in e["values"]]
        if e["type"]=="index": return self.evaluate(e["array"])[self.evaluate(e["index"])]
        if e["type"]=="binary":
            a,b=self.evaluate(e["left"]),self.evaluate(e["right"]); op=e["operator"]
            if op=="+": return a+b
            if op=="-": return a-b
            if op=="*": return a*b
            if op=="/":
                r=a/b; return int(r) if r.is_integer() else r
        raise RuntimeError("Unknown expression")
    def condition(self,c):
        a,b=self.evaluate(c["left"]),self.evaluate(c["right"])
        return {"mogs":a>b,"mogged_by":a<b,"larping":a==b}[c["operator"]]
    evaluate_condition=condition
