import ast

class SecurityScanner:
    def __init__(self, tree):
        self.tree = tree
        self.vulnerabilities = []

    def scan(self):
        """Scans the AST tree for potential security vulnerabilities."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                func = node.func
                # Check for cursor.execute() calls
                if isinstance(func, ast.Attribute):
                    method_name = func.attr
                    if method_name in ['execute', 'executemany']:
                        # Analyze the first argument of the function call
                        if node.args:
                            arg = node.args[0]
                            if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Mod):
                                # Detected string formatting with % operator
                                self.vulnerabilities.append({
                                    'type': 'SQL Injection',
                                    'line': node.lineno,
                                    'message': 'Potential SQL injection via string formatting.'
                                })
                            elif isinstance(arg, ast.Call) and getattr(arg.func, 'id', None) == 'format':
                                # Detected string formatting with .format()
                                self.vulnerabilities.append({
                                    'type': 'SQL Injection',
                                    'line': node.lineno,
                                    'message': 'Potential SQL injection via .format() method.'
                                })
                            elif isinstance(arg, ast.JoinedStr):
                                # Detected f-string usage
                                self.vulnerabilities.append({
                                    'type': 'SQL Injection',
                                    'line': node.lineno,
                                    'message': 'Potential SQL injection via f-string.'
                                })
                            # Additional checks can be added here
    def get_vulnerabilities(self):
        """Returns a list of found vulnerabilities."""
        return self.vulnerabilities
