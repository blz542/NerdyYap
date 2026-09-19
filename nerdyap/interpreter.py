class Interpreter:
    def __init__(self):
        self.variables = {}

    def run(self, statements):
        for statement in statements:

            if statement["type"] == "variable":
                value = self.evaluate(statement["value"])
                self.variables[statement["name"]] = value

            elif statement["type"] == "yap":
                value = self.evaluate(statement["value"])
                print(value)

            elif statement["type"] == "if":
                if self.evaluate_condition(statement["condition"]):
                    self.run(statement["if_statements"])

                elif statement["else_statements"] is not None:
                    self.run(statement["else_statements"])

    def evaluate(self, expression):

        if expression["type"] == "value":
            value = expression["value"]

            if isinstance(value, str) and value in self.variables:
                return self.variables[value]

            return value

        if expression["type"] == "binary":
            left = self.evaluate(expression["left"])
            right = self.evaluate(expression["right"])

            operator = expression["operator"]

            if operator == "+":
                return left + right

            if operator == "-":
                return left - right

            if operator == "*":
                return left * right

            if operator == "/":
                result = left / right

                if result.is_integer():
                    return int(result)
                
                return result
                            
            if operator == "mogs":
                return left > right

            if operator == "larping":
                return left == right

            raise RuntimeError(f"Unknown operator: {operator}")

        raise RuntimeError("Unknown expression")

    def evaluate_condition(self, condition):
        left = self.evaluate(condition["left"])
        right = self.evaluate(condition["right"])

        operator = condition["operator"]

        if operator == "mogs":
            return left > right

        if operator == "mogged_by":
            return left < right

        if operator == "larping":
            return left == right

        raise RuntimeError(f"Unknown comparison: {operator}")