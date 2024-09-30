import sys
from code_parser import CodeParser
from security_scanner import SecurityScanner
from performance_analyzer import PerformanceAnalyzer
from code_optimizer import CodeOptimizer
from report_generator import ReportGenerator

def main():
    if len(sys.argv) < 2:
        print("Please provide the path to the code file.")
        sys.exit(1)

    code_path = sys.argv[1]
    try:
        with open(code_path, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"File not found: {code_path}")
        sys.exit(1)

    parser = CodeParser(code)
    parser.parse()

    functions = parser.get_functions()
    classes = parser.get_classes()
    variables = parser.get_variables()

    print(f"Found {len(functions)} function(s).")
    print(f"Found {len(classes)} class(es).")
    print(f"Found {len(set(variables))} variable(s).")

    # Security analysis
    scanner = SecurityScanner()
    scanner.scan(parser.tree)
    vulnerabilities = scanner.get_vulnerabilities()

    if vulnerabilities:
        print("Security vulnerabilities found:")
        for vuln in vulnerabilities:
            print(f" - Line {vuln['line']}: {vuln['message']}")
    else:
        print("No security vulnerabilities found.")

    # Performance analysis
    performance_analyzer = PerformanceAnalyzer()
    performance_analyzer.visit(parser.tree)
    performance_analyzer.analyze(code)
    performance_report = performance_analyzer.get_report()

    print("Performance analysis report:")
    for report in performance_report:
        if report.get('error'):
            print(f" - Function {report['function']}: Error - {report['error']}")
        else:
            print(f" - Function {report['function']}: {report['time']} seconds per 1000 executions")

    # Code optimization
    optimizer = CodeOptimizer(code)
    optimizer.optimize()
    suggestions = optimizer.get_suggestions()

    if suggestions:
        print("Code style suggestions:")
        for suggestion in suggestions:
            print(f" - Line {suggestion['line']}, Column {suggestion['column']}: {suggestion['code']} {suggestion['message']}")
    else:
        print("No code style issues found.")

    # Collecting all results
    report_data = {
        'functions_found': len(functions),
        'classes_found': len(classes),
        'variables_found': len(set(variables)),
        'security_vulnerabilities': vulnerabilities,
        'performance_report': performance_report,
        'style_suggestions': suggestions
    }

    # Generate report
    report_generator = ReportGenerator(report_data)
    report_generator.generate_json_report()

if __name__ == '__main__':
    main()