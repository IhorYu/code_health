import ast

class CodeParser:
    def __init__(self, code):
        self.code = code
        self.tree = None

    def parse(self):
        """Parses the provided code and builds an abstract syntax tree."""
        try:
            self.tree = ast.parse(self.code)
        except SyntaxError as e:
            print(f"Syntax error: {e}")
            self.tree = None

    def get_functions(self):
        """Returns a list of function definitions found in the code."""
        if self.tree is None:
            return []
        return [node for node in ast.walk(self.tree) if isinstance(node, ast.FunctionDef)]

    def get_classes(self):
        """Returns a list of class definitions found in the code."""
        if self.tree is None:
            return []
        return [node for node in ast.walk(self.tree) if isinstance(node, ast.ClassDef)]

    def get_variables(self):
        """Returns a list of variable names found in the code."""
        if self.tree is None:
            return []
        return [node.id for node in ast.walk(self.tree) if isinstance(node, ast.Name)]
