import sys
from code_parser import CodeParser
from security_scanner import SecurityScanner

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
    scanner = SecurityScanner(parser.tree)
    scanner.scan()
    vulnerabilities = scanner.get_vulnerabilities()

    if vulnerabilities:
        print("Security vulnerabilities found:")
        for vuln in vulnerabilities:
            print(f" - Line {vuln['line']}: {vuln['message']}")
    else:
        print("No security vulnerabilities found.")

if __name__ == '__main__':
    main()
