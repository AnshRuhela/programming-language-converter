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
        cpp_args = [f"int {arg.strip()}" for arg in args.split(",") if arg]
        return {
            "type": "function",
            "name": name,
            "args": cpp_args,
            "indent": indent,
            "line": "    " * indent + f"__RETURN_TYPE__ {name}({', '.join(cpp_args)}) {{"
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
            return_types[func_name].add("string")
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
            "    " * indent + f'cout << "{prompt}";',
            "    " * indent + f"cin >> {var};"
        ]

    # Float input
    if re.match(r"^\w+\s*=\s*float\s*\(\s*input\s*\(['\"].*['\"]\)\s*\)$", stripped):
        var, input_call = stripped.split("=")
        var = var.strip()
        prompt = re.search(r"['\"](.*?)['\"]", input_call).group(1)
        return [
            "    " * indent + f"float {var};",
            "    " * indent + f'cout << "{prompt}";',
            "    " * indent + f"cin >> {var};"
        ]

    # String input
    if re.match(r"^\w+\s*=\s*input\s*\(['\"].*['\"]\)$", stripped):
        var, input_call = stripped.split("=")
        var = var.strip()
        prompt = re.search(r"['\"](.*?)['\"]", input_call).group(1)
        return [
            "    " * indent + f"string {var};",
            "    " * indent + f'cout << "{prompt}";',
            "    " * indent + f"getline(cin, {var});"
        ]

    # Print statement
    if stripped.startswith("print("):
        content = stripped[6:-1]
        return "    " * indent + f"cout << {content} << endl;"

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
        return "    " * indent + f"string {var.strip()} = {val.strip()};"

    # List assignment (e.g., arr = [1, 2, 3] or arr = ["a", "b"])
    if re.match(r"^\w+\s*=\s*\[.*\]$", stripped):
        var, val = stripped.split("=")
        var = var.strip()
        val = val.strip()[1:-1]  # Remove [ and ]
        elements = [e.strip() for e in val.split(",") if e.strip()]
        if not elements:
            return "    " * indent + f"vector<int> {var};"  # Default to int for empty vector
        # Determine type based on first element
        if re.match(r"^\d+\.\d+$", elements[0]):
            type_name = "float"
        elif re.match(r"^\d+$", elements[0]):
            type_name = "int"
        elif re.match(r"^['\"].*['\"]$", elements[0]):
            type_name = "string"
        else:
            type_name = "int"  # Default fallback
        return "    " * indent + f"vector<{type_name}> {var} {{{val}}};"

    # Min function call (e.g., min(a, b) -> std::min(a, b))
    if re.match(r"^min\s*\(\s*\w+\s*,\s*\w+\s*\)$", stripped):
        args = stripped[4:-1].strip()  # Extract content inside min()
        return "    " * indent + f"std::min({args});"

    # Max function call (e.g., max(a, b) -> std::max(a, b))
    if re.match(r"^max\s*\(\s*\w+\s*,\s*\w+\s*\)$", stripped):
        args = stripped[4:-1].strip()  # Extract content inside max()
        return "    " * indent + f"std::max({args});"

    # For loop
    if stripped.startswith("for") and "range" in stripped:
        var = re.search(r"for\s+(\w+)\s+in", stripped).group(1)
        limit = re.search(r"range\((\d+)\)", stripped).group(1)
        return "    " * indent + f"for (int {var} = 0; {var} < {limit}; {var}++) {{"

    # If statement
    if stripped.startswith("if"):
        condition = stripped[2:].strip().rstrip(":")
        return "    " * indent + f"if ({condition}) {{"

    # Elif statement
    if stripped.startswith("elif"):
        condition = stripped[4:].strip().rstrip(":")
        return "    " * indent + f"else if ({condition}) {{"

    # Else statement
    if stripped == "else:":
        return "    " * indent + "else {"

    # While loop
    if stripped.startswith("while"):
        condition = stripped[5:].strip().rstrip(":")
        return "    " * indent + f"while ({condition}) {{"

    # Math function call (e.g., math.ceil(3.4) -> ceil(3.4))
    if re.match(r"^math\.\w+\s*\(.*\)$", stripped):
        func_call = re.sub(r"^math\.", "", stripped)  # Remove math. prefix
        return "    " * indent + f"{func_call};"

    # Function call
    if re.match(r"^\w+\s*\(.*\)$", stripped) and not stripped.startswith(("def ", "print(", "int(", "float(", "input(")):
        return "    " * indent + f"{stripped};"

    # General assignment (e.g., x = x + 1)
    if re.match(r"^\w+\s*=\s*.+$", stripped):
        return "    " * indent + f"{stripped};"

    # Fallback for unhandled lines
    return "    " * indent + "// " + stripped

def convert_file(input_file, output_file):
    # Read Python code
    with open(input_file, "r") as f:
        lines = f.readlines()

    # C++ headers
    output = [
        "#include <iostream>",
        "#include <string>",
    ]
    # Check for math functions or import math
    has_math = any(line.strip().startswith("import math") or re.match(r"^\s*math\.\w+\s*\(.*\)$", line.strip()) for line in lines)
    has_vector = any(re.match(r"^\s*\w+\s*=\s*\[.*\]$", line.strip()) for line in lines)
    has_algorithm = any(re.match(r"^\s*min\s*\(\s*\w+\s*,\s*\w+\s*\)$", line.strip()) or re.match(r"^\s*max\s*\(\s*\w+\s*,\s*\w+\s*\)$", line.strip()) for line in lines)
    if has_math:
        output.append("#include <cmath>")
    if has_vector:
        output.append("#include <vector>")
    if has_algorithm:
        output.append("#include <algorithm>")
    output.append("using namespace std;")
    output.append("")

    func_code = []  # Function code
    main_code = ["int main() {"]  # Main function
    block_indents = [0]  # Track main block indents
    func_block_indents = []  # Track function block indents
    curr_func_indent = None  # Current function indent
    curr_func_name = None  # Current function name
    return_types = {}  # Track return types
    func_defs = []  # Store function definitions
    last_indent = 0  # Last line's indent

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import math"):
            continue  # Skip the import line
        indent = (len(line) - len(line.lstrip())) // 4 if stripped else last_indent

        # Close main blocks if indent decreases
        while block_indents and indent < block_indents[-1]:
            block_indents.pop()
            main_code.append("    " * indent + "}")

        # Close function blocks if indent decreases
        if curr_func_indent is not None and stripped:
            while func_block_indents and indent < func_block_indents[-1]:
                func_block_indents.pop()
                func_code.append("    " * indent + "}")
            if indent <= curr_func_indent:
                func_code.append("    " * curr_func_indent + "}")
                # Set return type
                return_type = "void"
                if curr_func_name in return_types:
                    types = return_types[curr_func_name]
                    return_type = "float" if "float" in types else "int" if "int" in types else "string" if "string" in types else "void"
                # Update function definition
                for fdef in func_defs:
                    if fdef["name"] == curr_func_name:
                        fdef["final_line"] = fdef["line"].replace("__RETURN_TYPE__", return_type)
                curr_func_indent = None
                curr_func_name = None
                func_block_indents = []

        if not stripped:
            continue

        last_indent = indent

        # Handle function definition
        if stripped.startswith("def "):
            curr_func_indent = indent
            curr_func_name = stripped.split("(")[0].replace("def ", "").strip()
            return_types[curr_func_name] = set()
            translated = translate_line(line, indent, True, curr_func_name, return_types)
            func_defs.append(translated)
            func_code.append(translated["line"])
            continue

        # Translate line
        translated = translate_line(line, indent, curr_func_indent is not None, curr_func_name, return_types)
        target = func_code if curr_func_indent is not None else main_code
        if isinstance(translated, list):
            target.extend(translated)
        else:
            target.append(translated)

        # Track new blocks
        if isinstance(translated, str) and translated.endswith("{"):
            if curr_func_indent is not None and not stripped.startswith("def "):
                func_block_indents.append(indent + 1)
            elif not stripped.startswith("def "):
                block_indents.append(indent + 1)

    # Close remaining function
    if curr_func_indent is not None:
        while func_block_indents:
            indent = func_block_indents.pop()
            func_code.append("    " * (indent - 1) + "}")
        func_code.append("    " * curr_func_indent + "}")
        return_type = "void"
        if curr_func_name in return_types:
            types = return_types[curr_func_name]
            return_type = "float" if "float" in types else "int" if "int" in types else "string" if "string" in types else "void"
        for fdef in func_defs:
            if fdef["name"] == curr_func_name:
                fdef["final_line"] = fdef["line"].replace("__RETURN_TYPE__", return_type)

    # Close remaining main blocks
    while len(block_indents) > 1:
        indent = block_indents.pop()
        main_code.append("    " * (indent - 1) + "}")

    # Finalize main
    main_code.append("    return 0;")
    main_code.append("}")

    # Replace function placeholders
    final_func_code = []
    for line in func_code:
        if "__RETURN_TYPE__" in line:
            for fdef in func_defs:
                if fdef["line"] == line:
                    final_func_code.append(fdef["final_line"])
                    break
        else:
            final_func_code.append(line)

    # Combine output
    output.extend(final_func_code)
    output.append("")
    output.extend(main_code)

    # Write C++ code
    with open(output_file, "w") as f:
        f.write("\n".join(output))

    print(f"✅ Converted to {output_file}")

if __name__ == "__main__":
    convert_file("input.py", "output.cpp")
    