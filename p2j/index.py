import re

def translate_line(line, indent, in_function, func_name, return_types):
    line = line.rstrip()
    stripped = line.strip()

    # Handle comments
    if stripped.startswith("#"):
        return "    " * indent + "// " + stripped[1:].strip()

    # Function definition
    if stripped.startswith("def "):
        func_def = stripped[4:].rstrip(":")
        name, args = func_def.split("(")
        args = args.rstrip(")")
        cpp_args = [f"String {arg.strip()}" for arg in args.split(",") if arg]
        return {
            "type": "function",
            "name": name,
            "args": cpp_args,
            "indent": indent,
            "line": "    " * indent + f"public static void {name}({', '.join(cpp_args)}) {{"
        }

    # Return statement
    if stripped.startswith("return "):
        expr = stripped[7:].strip()
        # Guess return type
        if re.match(r"^\d+\.\d+$", expr):
            return_types[func_name].add("float")
        elif re.match(r"^\d+$", expr):
            return_types[func_name].add("int")
        elif re.match(r"^['\"].*['\"]$", expr):
            return_types[func_name].add("String")
        else:
            return_types[func_name].add("void")
        return "    " * indent + f"return {expr};"

    # Integer input
    if re.match(r"^\w+\s*=\s*int\s*\(\s*input\s*\(['\"].*['\"]\)\s*\)$", stripped):
        var, input_call = stripped.split("=")
        var = var.strip()
        prompt = re.search(r"['\"](.*?)['\"]", input_call).group(1)
        return [
            "    " * indent + f"int {var};",
            "    " * indent + f'System.out.print("{prompt}");',
            "    " * indent + f"{var} = scanner.nextInt();"
        ]

    # Float input
    if re.match(r"^\w+\s*=\s*float\s*\(\s*input\s*\(['\"].*['\"]\)\s*\)$", stripped):
        var, input_call = stripped.split("=")
        var = var.strip()
        prompt = re.search(r"['\"](.*?)['\"]", input_call).group(1)
        return [
            "    " * indent + f"float {var};",
            "    " * indent + f'System.out.print("{prompt}");',
            "    " * indent + f"{var} = scanner.nextFloat();"
        ]

    # String input
    if re.match(r"^\w+\s*=\s*input\s*\(['\"].*['\"]\)$", stripped):
        var, input_call = stripped.split("=")
        var = var.strip()
        prompt = re.search(r"['\"](.*?)['\"]", input_call).group(1)
        return [
            "    " * indent + f"String {var};",
            "    " * indent + f'System.out.print("{prompt}");',
            "    " * indent + f"{var} = scanner.nextLine();"
        ]

    # Print statement
    if stripped.startswith("print("):
        content = stripped[6:-1]
        return "    " * indent + f"System.out.println({content});"

    # Float assignment
    if re.match(r"^\w+\s*=\s*\d*\.\d+$", stripped):
        var, val = stripped.split("=")
        return "    " * indent + f"float {var.strip()} = {val.strip()};"

    # Integer assignment
    if re.match(r"^\w+\s*=\s*\d+$", stripped):
        var, val = stripped.split("=")
        return "    " * indent + f"int {var.strip()} = {val.strip()};"

    # String assignment
    if re.match(r"^\w+\s*=\s*['\"].*['\"]$", stripped):
        var, val = stripped.split("=")
        return "    " * indent + f"String {var.strip()} = {val.strip()};"

    # For loop
    if stripped.startswith("for") and "range" in stripped:
        var = re.search(r"for\s+(\w+)\s+in", stripped).group(1)
        limit = re.search(r"range\((\d+)\)", stripped).group(1)
        return "    " * indent + f"for (int {var} = 0; {var} < {limit}; {var}++) {{"

    # If statement
    if stripped.startswith("if"):
        condition = stripped[2:].strip().rstrip(":")
        return "    " * indent + f"if ({condition}) {{"

    # While loop
    if stripped.startswith("while"):
        condition = stripped[5:].strip().rstrip(":")
        return "    " * indent + f"while ({condition}) {{"

    # Else
    if stripped == "else":
        return "    " * indent + "else {"

    # General assignment (e.g., x = x + 1)
    if re.match(r"^\w+\s*=\s*.+$", stripped):
        return "    " * indent + f"{stripped};"

    # Fallback for unhandled lines
    return "    " * indent + "// " + stripped

def convert_file(input_file, output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    output = [
        "import java.util.Scanner;",
        "public class Main {",
        "    public static void main(String[] args) {",
        "        Scanner scanner = new Scanner(System.in);",
        ""
    ]

    func_code = []
    main_code = []
    block_indents = [0]
    curr_func_indent = None
    curr_func_name = None
    return_types = {}

    for line in lines:
        stripped = line.strip()
        indent = (len(line) - len(line.lstrip())) // 4 if stripped else 0

        if not stripped:
            continue

        # Handle function definition
        if stripped.startswith("def "):
            curr_func_indent = indent
            curr_func_name = stripped.split("(")[0].replace("def ", "").strip()
            return_types[curr_func_name] = set()
            translated = translate_line(line, indent, True, curr_func_name, return_types)
            func_code.append(translated["line"] if isinstance(translated, str) else "\n".join(translated))
            continue

        # Translate line
        translated = translate_line(line, indent, curr_func_indent is not None, curr_func_name, return_types)
        target = func_code if curr_func_indent is not None else main_code
        target.append(translated if isinstance(translated, str) else "\n".join(translated))

    # Close remaining functions
    if curr_func_indent is not None:
        func_code.append("    }")

    # Finalize main
    main_code.append("    }")
    main_code.append("}")

    output.extend(func_code)
    output.append("")
    output.extend(main_code)

    with open(output_file, "w") as f:
        f.write("\n".join(output))

    print(f"✅ Converted to {output_file}")

if __name__ == "__main__":
    convert_file("sample_input.py", "converted_code.java")
