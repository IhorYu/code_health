import sys
from code_parser import CodeParser

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

if __name__ == '__main__':
    main()
