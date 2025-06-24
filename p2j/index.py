import re
from collections import defaultdict

def translate_line(line, indent, in_function, func_name, return_types, block_stack, local_vars, main_code, func_code):
    line = line.rstrip()
    stripped = line.strip()
    if not stripped:
        return [""]

    # Skip Python-specific main check
    if stripped.startswith("if __name__ == \"__main__\":"):
        block_stack.append(("main", indent, None))
        return [""]

    # Handle comments
    if stripped.startswith("#"):
        return ["    " * indent + "// " + stripped[1:].strip()]

    # Function definition
    if stripped.startswith("def "):
        func_def = stripped[4:].rstrip(":")
        name, args = func_def.split("(") if "(" in func_def else (func_def, "")
        args = args.rstrip(")")
        java_args = [f"int {arg.strip()}" for arg in args.split(",") if arg]
        block_stack.append(("function", indent, name))
        return_types[name] = set(["void"])
        return ["    " * indent + f"public static void {name}({', '.join(java_args)}) {{", ""]

    # Return statement
    if stripped.startswith("return "):
        expr = stripped[7:].strip()
        if func_name:
            if re.match(r"^\d+\.\d+$", expr):
                return_types[func_name].add("float")
            elif re.match(r"^\d+$", expr):
                return_types[func_name].add("int")
            elif re.match(r"^['\"].*['\"]$", expr):
                return_types[func_name].add("String")
            elif expr in ("True", "False"):
                return_types[func_name].add("boolean")
            elif expr.startswith("["):
                return_types[func_name].add("ArrayList<String>")
            elif re.match(r"^\w+\s*[\+\-\*/]\s*\w+$", expr):
                return_types[func_name].add("int")
            else:
                for var_line in main_code + func_code:
                    if var_line.strip().startswith(f"int {expr}"):
                        return_types[func_name].add("int")
                    elif var_line.strip().startswith(f"float {expr}"):
                        return_types[func_name].add("float")
                    elif var_line.strip().startswith(f"String {expr}"):
                        return_types[func_name].add("String")
                    elif var_line.strip().startswith(f"boolean {expr}"):
                        return_types[func_name].add("boolean")
                    elif var_line.strip().startswith(f"ArrayList<String> {expr}"):
                        return_types[func_name].add("ArrayList<String>")
                if not return_types[func_name] - {"void"}:
                    return_types[func_name].add("int")
        return ["    " * indent + f"return {expr.replace('True', 'true').replace('False', 'false')};"]

    # Integer input
    if re.match(r"^\w+\s*=\s*int\s*\(\s*input\s*\((['\"][^'\"]*['\"])?\s*\)\s*\)$", stripped):
        var = re.match(r"^(\w+)\s*=\s*", stripped).group(1)
        prompt = re.search(r"['\"](.*?)['\"]", stripped).group(1) if re.search(r"['\"](.*?)['\"]", stripped) else ""
        local_vars.add(var)
        lines = ["    " * indent + f"int {var};"]
        if prompt:
            lines.append("    " * indent + f"System.out.print(\"{prompt}\");")
        lines.append("    " * indent + f"{var} = scanner.nextInt();")
        lines.append("    " * indent + "scanner.nextLine(); // Clear buffer")
        lines.append("")
        return lines

    # Float input
    if re.match(r"^\w+\s*=\s*float\s*\(\s*input\s*\((['\"][^'\"]*['\"])?\s*\)\s*\)$", stripped):
        var = re.match(r"^(\w+)\s*=\s*", stripped).group(1)
        prompt = re.search(r"['\"](.*?)['\"]", stripped).group(1) if re.search(r"['\"](.*?)['\"]", stripped) else ""
        local_vars.add(var)
        lines = ["    " * indent + f"float {var};"]
        if prompt:
            lines.append("    " * indent + f"System.out.print(\"{prompt}\");")
        lines.append("    " * indent + f"{var} = scanner.nextFloat();")
        lines.append("    " * indent + "scanner.nextLine(); // Clear buffer")
        lines.append("")
        return lines

    # String input
    if re.match(r" impossibile \w+\s*=\s*input\s*\((['\"][^'\"]*['\"])?\s*\)$", stripped):
        var = re.match(r"^(\w+)\s*=\s*", stripped).group(1)
        prompt = re.search(r"['\"](.*?)['\"]", stripped).group(1) if re.search(r"['\"](.*?)['\"]", stripped) else ""
        local_vars.add(var)
        lines = ["    " * indent + f"String {var};"]
        if prompt:
            lines.append("    " * indent + f"System.out.print(\"{prompt}\");")
        lines.append("    " * indent + f"{var} = scanner.nextLine();")
        lines.append("")
        return lines

    # Print statement with f-strings
    if stripped.startswith("print("):
        content = stripped[6:-1].strip()
        if content.startswith("f'") or content.startswith('f"'):
            raw_content = content[2:-1]
            content = re.sub(r"\{(\w+)\}", "%s", raw_content)
            vars = re.findall(r"\{(\w+)\}", raw_content)
            format_specifiers = ["%d" if v in local_vars and any(l.strip().startswith(f"int {v}") for l in main_code + func_code)
                                else "%.2f" if v in local_vars and any(l.strip().startswith(f"float {v}") for l in main_code + func_code)
                                else "%s" for v in vars]
            content = re.sub(r"%s", lambda m, fs=format_specifiers: fs.pop(0), content, len(format_specifiers))
            return ["    " * indent + f"System.out.printf(\"{content}\\n\", {', '.join(vars)});", ""]
        else:
            return ["    " * indent + f"System.out.println({content});", ""]

    # List declaration
    if re.match(r"^\w+\s*=\s*\[.*\]$", stripped):
        var = re.match(r"^(\w+)\s*=\s*", stripped).group(1)
        val = stripped.split("=")[1].strip()
        local_vars.add(var)
        if val == "[]":
            return ["    " * indent + f"ArrayList<String> {var} = new ArrayList<>();", ""]
        else:
            elements = val[1:-1].split(",")
            lines = ["    " * indent + f"ArrayList<String> {var} = new ArrayList<>();"]
            lines.extend(["    " * indent + f"{var}.add({e.strip()});" for e in elements if e.strip()])
            lines.append("")
            return lines

    # Arithmetic assignment
    if re.match(r"^\w+\s*(\+=|-=|\*=|/=|//=|\%=)\s*.+$", stripped):
        var = re.match(r"^(\w+)", stripped).group(1)
        op = re.search(r"(\+=|-=|\*=|/=|//=|\%=)", stripped).group(1)
        expr = stripped.split(op)[1].strip()
        if var not in local_vars:
            local_vars.add(var)
            return ["    " * indent + f"int {var} = 0;", "    " * indent + f"{var} {op} {expr};", ""]
        return ["    " * indent + f"{var} {op} {expr};", ""]

    # Float assignment
    if re.match(r"^\w+\s*=\s*\d*\.\d+f?$", stripped):
        var = re.match(r"^(\w+)\s*=\s*", stripped).group(1)
        val = stripped.split("=")[1].strip()
        local_vars.add(var)
        return ["    " * indent + f"float {var} = {val.rstrip('f')}f;", ""]

    # Integer assignment
    if re.match(r"^\w+\s*=\s*\d+$", stripped):
        var = re.match(r"^(\w+)\s*=\s*", stripped).group(1)
        val = stripped.split("=")[1].strip()
        local_vars.add(var)
        return ["    " * indent + f"int {var} = {val};", ""]

    # String assignment
    if re.match(r"^\w+\s*=\s*['\"].*['\"]$", stripped):
        var = re.match(r"^(\w+)\s*=\s*", stripped).group(1)
        val = stripped.split("=")[1].strip()
        local_vars.add(var)
        return ["    " * indent + f"String {var} = {val};", ""]

    # Boolean assignment
    if re.match(r"^\w+\s*=\s*(True|False)$", stripped):
        var = re.match(r"^(\w+)\s*=\s*", stripped).group(1)
        val = stripped.split("=")[1].strip()
        local_vars.add(var)
        return ["    " * indent + f"boolean {var} = {val.lower()};", ""]

    # For loop with range
    if stripped.startswith("for") and "range" in stripped:
        var = re.search(r"for\s+(\w+)\s+in", stripped).group(1)
        range_match = re.search(r"range\(([^)]+)\)", stripped)
        range_args = range_match.group(1).split(",")
        if len(range_args) == 1:
            start, stop, step = "0", range_args[0].strip(), "1"
        elif len(range_args) == 2:
            start, stop, step = range_args[0].strip(), range_args[1].strip(), "1"
        else:
            start, stop, step = range_args[0].strip(), range_args[1].strip(), range_args[2].strip()
        local_vars.add(var)
        block_stack.append(("for", indent, None))
        # Simplify stop condition (e.g., n + 1 -> <= n)
        if re.match(r"^\w+\s*\+\s*1$", stop.strip()):
            stop = stop.split("+")[0].strip()
            condition = f"{var} <= {stop}"
        else:
            condition = f"{var} < {stop}"
        step = "++" if step == "1" else f"+= {step}"
        return ["    " * indent + f"for (int {var} = {start}; {condition}; {var} {step}) {{", ""]

    # If statement
    if stripped.startswith("if"):
        condition = stripped[2:].strip().rstrip(":").replace(" or ", " || ").replace(" and ", " && ")
        block_stack.append(("if", indent, None))
        return ["    " * indent + f"if ({condition}) {{", ""]

    # Elif statement
    if stripped.startswith("elif"):
        condition = stripped[4:].strip().rstrip(":").replace(" or ", " || ").replace(" and ", " && ")
        block_stack.append(("if", indent, None))
        return ["    " * (indent - 1) + "} else if (" + condition + ") {", ""]

    # Else statement
    if stripped.startswith("else"):
        block_stack.append(("if", indent, None))
        return ["    " * (indent - 1) + "} else {", ""]

    # While loop
    if stripped.startswith("while"):
        condition = stripped[5:].strip().rstrip(":").replace(" or ", " || ").replace(" and ", " && ")
        block_stack.append(("while", indent, None))
        return ["    " * indent + f"while ({condition}) {{", ""]

    # Break and Continue
    if stripped in ("break", "continue"):
        return ["    " * indent + f"{stripped};", ""]

    # Pass
    if stripped == "pass":
        return [""]

    # General assignment or function call
    if re.match(r"^\w+\s*=\s*.+$", stripped):
        var = re.match(r"^(\w+)\s*=\s*", stripped).group(1)
        expr = stripped.split("=", 1)[1].strip()
        if var not in local_vars:
            local_vars.add(var)
            return ["    " * indent + f"int {var} = {expr};", ""]
        return ["    " * indent + f"{var} = {expr};", ""]

    # Fallback for unhandled lines
    return ["    " * indent + f"// TODO: Unhandled: {stripped}", ""]

def convert_file(input_file, output_file):
    global main_code, func_code
    main_code = []
    func_code = []
    with open(input_file, "r", encoding='utf-8') as f:
        lines = f.readlines()

    output = [
        "import java.util.*;",
        "",
        "public class Main {",
        "    private static Scanner scanner = new Scanner(System.in);",
        ""
    ]

    block_stack = []
    return_types = defaultdict(set)
    local_vars = set()
    curr_func_name = None
    current_func_lines = []
    last_section = None  # Track section for blank line insertion (e.g., declarations, input, loops)

    for line in lines:
        stripped = line.strip()
        indent = (len(line) - len(line.lstrip())) // 2
        if not stripped:
            continue

        # Close blocks if indentation decreases
        while block_stack and indent <= block_stack[-1][1]:
            block_type, block_indent, block_name = block_stack.pop()
            target = current_func_lines if curr_func_name else main_code
            if block_type == "function" and indent <= block_indent:
                func_code.extend(current_func_lines)
                func_code.append("    " * block_indent + "}")
                func_code.append("")
                current_func_lines = []
                curr_func_name = None
            elif block_type != "function":
                target.append("    " * block_indent + "}")
                target.append("")

        # Determine section for blank line insertion
        section = None
        if stripped.startswith("def "):
            section = "function"
        elif re.match(r"^\w+\s*=\s*(int|float)\s*\(\s*input\s*\(.+\)\s*\)$", stripped):
            section = "input"
        elif stripped.startswith("print("):
            section = "output"
        elif stripped.startswith(("for ", "while ", "if ", "elif ", "else")):
            section = "control"
        elif re.match(r"^\w+\s*=\s*.+$", stripped):
            section = "declaration"

        # Insert blank line before new section
        target = current_func_lines if curr_func_name else main_code
        if section and section != last_section and target and target[-1].strip():
            target.append("")
        last_section = section

        # Handle function definition
        if stripped.startswith("def "):
            if current_func_lines:
                func_code.extend(current_func_lines)
                if block_stack and block_stack[-1][0] == "function":
                    func_code.append("    " * block_stack[-1][1] + "}")
                    func_code.append("")
                current_func_lines = []
            curr_func_name = stripped.split("(")[0].replace("def ", "").strip()
            translated = translate_line(line, indent, True, curr_func_name, return_types, block_stack, local_vars, main_code, func_code)
            current_func_lines.extend(translated if isinstance(translated, list) else [translated])
            local_vars = set()
            continue

        # Translate line
        translated = translate_line(line, indent, bool(curr_func_name), curr_func_name, return_types, block_stack, local_vars, main_code, func_code)
        target.extend(translated if isinstance(translated, list) else [translated])

    # Close any remaining function
    if current_func_lines:
        func_code.extend(current_func_lines)
        if block_stack and block_stack[-1][0] == "function":
            func_code.append("    " * block_stack[-1][1] + "}")
            func_code.append("")
        block_stack = [b for b in block_stack if b[0] != "function"]

    # Close any remaining blocks
    while block_stack:
        block_type, block_indent, _ = block_stack.pop()
        main_code.append("    " * block_indent + "}")
        main_code.append("")

    # Update function return types
    for func_name, types in return_types.items():
        best_type = ("String" if "String" in types else
                     "int" if "int" in types else
                     "float" if "float" in types else
                     "boolean" if "boolean" in types else
                     "ArrayList<String>" if "ArrayList<String>" in types else
                     "void")
        if best_type != "void":
            func_code[:] = [line.replace(f"void {func_name}(", f"{best_type} {func_name}(")
                           for line in func_code]
            if best_type == "ArrayList<String>":
                for i, line in enumerate(func_code):
                    if line.strip().startswith("return ["):
                        elements = re.findall(r"['\"]([^'\"]+)['\"]", line)
                        indent_level = (len(line) - len(line.lstrip())) // 4
                        func_code[i] = "    " * indent_level + f"ArrayList<String> result = new ArrayList<>();"
                        func_code[i:i+1] = [func_code[i]] + ["    " * indent_level + f"result.add(\"{e}\");" for e in elements] + ["    " * indent_level + "return result;", ""]
            if best_type == "String" and ("int" in types or "float" in types):
                func_code[:] = [line.replace(f"return {v};", f"return String.valueOf({v});")
                               for line, v in [(line, re.match(r"return ([\w\d\.\+\-\*/]+);", line))
                                              for line in func_code] if v]

    # Finalize output
    if main_code:
        output.append("    public static void main(String[] args) {")
        output.extend([line for line in main_code if line.strip() or line == ""])
        output.append("    }")
        output.append("")
    output.extend([line for line in func_code if line.strip() or line == ""])
    output.append("}")

    # Remove consecutive blank lines
    final_output = []
    last_was_blank = False
    for line in output:
        is_blank = line.strip() == ""
        if is_blank and last_was_blank:
            continue
        final_output.append(line)
        last_was_blank = is_blank

    with open(output_file, "w", encoding='utf-8') as f:
        f.write("\n".join(final_output))

    print(f"Converted to {output_file}")

if __name__ == "__main__":
    convert_file("test.py", "converted_code.java")  