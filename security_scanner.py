import ast

class SecurityScanner(ast.NodeVisitor):
    def __init__(self):
        self.vulnerabilities = []
        self.assignments = {}  # Mapping of variable names to their assigned values

    def visit_Assign(self, node):
        """Visit assignment nodes to track variable assignments."""
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            value = node.value
            self.assignments[var_name] = value
        self.generic_visit(node)

    def visit_Call(self, node):
        """Visit function calls to detect vulnerabilities."""
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            if method_name in ['execute', 'executemany']:
                # Analyze arguments passed to execute()
                if node.args:
                    arg = node.args[0]
                    query_node = self.resolve_value(arg)
                    if self.is_potentially_unsafe(query_node):
                        self.vulnerabilities.append({
                            'type': 'SQL Injection',
                            'line': node.lineno,
                            'message': 'Potential SQL injection detected.'
                        })
        self.generic_visit(node)

    def resolve_value(self, node):
        """Resolves the actual value of a node, handling variables."""
        if isinstance(node, ast.Name):
            var_name = node.id
            return self.assignments.get(var_name, None)
        return node

    def is_potentially_unsafe(self, node):
        """Checks if the node represents a potentially unsafe SQL query."""
        if node is None:
            return False
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
            # Detected string formatting with % operator
            return True
        elif isinstance(node, ast.Call) and getattr(node.func, 'attr', '') == 'format':
            # Detected string formatting with .format()
            return True
        elif isinstance(node, ast.JoinedStr):
            # Detected f-string usage
            return True
        return False

    def scan(self, tree):
        """Initiates the scanning process."""
        self.visit(tree)

    def get_vulnerabilities(self):
        """Returns a list of found vulnerabilities."""
        return self.vulnerabilities
