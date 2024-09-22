import ast
import timeit

class PerformanceAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.performance_report = []

    def visit_FunctionDef(self, node):
        """Collect function definitions."""
        self.functions.append(node)
        self.generic_visit(node)

    def analyze(self, code):
        """Analyze performance of collected functions."""
        local_namespace = {}
        try:
            exec(code, local_namespace)
        except Exception as e:
            for func in self.functions:
                self.performance_report.append({
                    'function': func.name,
                    'time': None,
                    'error': f"Error executing code: {str(e)}"
                })
            return

        for func in self.functions:
            func_name = func.name

            # Define a wrapper function that suppresses stdout
            wrapper_code = f"""
                def _wrapped_{func_name}():
                import sys
                import io
                from contextlib import redirect_stdout
                f = io.StringIO()
                with redirect_stdout(f):
                return {func_name}()
                """
            try:
                # Add the wrapper function to local_namespace
                exec(wrapper_code, local_namespace)
                stmt = f"_wrapped_{func_name}()"
                timer = timeit.Timer(stmt=stmt, globals=local_namespace)
                exec_time = timer.timeit(number=1000)
                self.performance_report.append({
                    'function': func_name,
                    'time': exec_time
                })
            except Exception as e:
                self.performance_report.append({
                    'function': func_name,
                    'time': None,
                    'error': str(e)
                })

    def get_report(self):
        """Returns the performance analysis report."""
        return self.performance_report
