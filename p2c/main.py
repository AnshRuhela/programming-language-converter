import re

def translate_line(line, indent, in_function, func_name, return_types, local_vars):
    line = line.rstrip()
    stripped = line.strip()
    
    # Replace Python logical operators with C equivalents
    stripped = stripped.replace(" and ", " && ").replace(" or ", " || ")
    
    # Handle comments
    if stripped.startswith("#"):
        return "    " * indent + "// " + stripped[1:].strip()
    
    # Handle function definitions
    if stripped.startswith("def "):
        func_def = stripped[4:].rstrip(":")
        name_part = func_def.split("(")[0].strip()
        args_part = func_def.split("(")[1].split(")")[0].strip()
        arg_list = [arg.strip() for arg in args_part.split(",") if arg]
        c_args = []
        for arg in arg_list:
            # Handle typed parameters (x: int)
            if ":" in arg:
                arg_name, arg_type = map(str.strip, arg.split(":"))
                if arg_type == "int":
                    c_args.append(f"int {arg_name}")
                    local_vars[arg_name] = "int"
                elif arg_type == "float":
                    c_args.append(f"float {arg_name}")
                    local_vars[arg_name] = "float"
                elif arg_type == "str":
                    c_args.append(f"char* {arg_name}")
                    local_vars[arg_name] = "char*"
                else:
                    c_args.append(f"int {arg_name}")  # default
                    local_vars[arg_name] = "int"
            else:
                c_args.append(f"int {arg}")  # default to int
                local_vars[arg] = "int"
        return {
            "type": "function",
            "name": name_part,
            "args": c_args,
            "indent": indent,
            "line": "    " * indent + f"_RETURN_TYPE_ {name_part}({', '.join(c_args)}) {{"
        }
    
    # Handle return statements
    if stripped.startswith("return "):
        expr = stripped[7:].strip()
        inferred_type = "void"

        if re.match(r"^\d+\.\d+$", expr):
            inferred_type = "float"
        elif re.match(r"^\d+$", expr):
            inferred_type = "int"
        elif re.match(r"^['\"].*['\"]$", expr):
            inferred_type = "char*"
        elif expr in local_vars:
            inferred_type = local_vars[expr]
        elif re.match(r"^\w+\s*[\+\-\*/]\s*\w+$", expr):  # like a + b
            tokens = re.split(r"[\+\-\*/]", expr)
            types = {local_vars.get(tok.strip(), "int") for tok in tokens}
            if "float" in types:
                inferred_type = "float"
            elif "int" in types:
                inferred_type = "int"
            elif "char*" in types:
                inferred_type = "char*"

        if func_name:  # Only track return types for functions
            return_types[func_name].add(inferred_type)
        return "    " * indent + f"return {expr};"
    
    # Handle increment/decrement operators (x += 1, x -= 1 )
    if re.match(r"^\w+\s*(\+\=|\-\=)\s*1$", stripped):
        return "    " * indent + f"{stripped};"
        
    # Integer input
    if re.match(r"^\w+\s*=\s*int\s*\(\s*input\s*\(['\"].*['\"]\)\s*\)$", stripped):
        var, input_call = stripped.split("=")
        var = var.strip()
        local_vars[var] = "int"
        prompt = re.search(r"['\"](.*?)['\"]", input_call).group(1)
        return [
            "    " * indent + f"int {var};",
            "    " * indent + f'printf("{prompt}");',
            "    " * indent + f"scanf(\"%d\", &{var});"
        ]

    # Float input
    if re.match(r"^\w+\s*=\s*float\s*\(\s*input\s*\(['\"].*['\"]\)\s*\)$", stripped):
        var, input_call = stripped.split("=")
        var = var.strip()
        local_vars[var] = "float"
        prompt = re.search(r"['\"](.*?)['\"]", input_call).group(1)
        return [
            "    " * indent + f"float {var};",
            "    " * indent + f'printf("{prompt}");',
            "    " * indent + f"scanf(\"%f\", &{var});"
        ]

    # String input
    if re.match(r"^\w+\s*=\s*input\s*\(['\"].*['\"]\)$", stripped):
        var, input_call = stripped.split("=")
        var = var.strip()
        local_vars[var] = "char*"
        prompt = re.search(r"['\"](.*?)['\"]", input_call).group(1)
        return [
            "    " * indent + f"char {var}[100];",
            "    " * indent + f'printf("{prompt}");',
            "    " * indent + f"scanf(\"%s\", {var});"
        ]

    # Print statement
    if stripped.startswith("print("):
        content = stripped[6:-1].strip()

        if re.match(r"^['\"].*['\"]$", content):
            return "    " * indent + f'printf({content});'

        if content in local_vars:
            var_type = local_vars[content]
            fmt = "%d" if var_type == "int" else "%f" if var_type == "float" else "%s"
            return "    " * indent + f'printf("{fmt}\\n", {content});'

        if re.match(r"^\d+$", content):
            return "    " * indent + f'printf("%d\\n", {content});'
        elif re.match(r"^\d+\.\d+$", content):
            return "    " * indent + f'printf("%f\\n", {content});'

        if re.match(r"^\w+\s*[\+\-\*/]\s*\w+$", content):
            tokens = re.split(r"[\+\-\*/]", content)
            var_types = [local_vars.get(tok.strip(), "int") for tok in tokens]
            if "char*" in var_types:
                fmt = "%s"
            elif "float" in var_types:
                fmt = "%f"
            else:
                fmt = "%d"
            return "    " * indent + f'printf("{fmt}\\n", {content});'

        return "    " * indent + f'printf("%d\\n", {content});'

    # Float assignment
    if re.match(r"^\w+\s*=\s*\d*\.\d+$", stripped):
        var, val = stripped.split("=")
        var = var.strip()
        local_vars[var] = "float"
        return "    " * indent + f"float {var} = {val.strip()};"

    # Integer assignment
    if re.match(r"^\w+\s*=\s*\d+$", stripped):
        var, val = stripped.split("=")
        var = var.strip()
        local_vars[var] = "int"
        return "    " * indent + f"int {var} = {val.strip()};"

    # String assignment
    if re.match(r"^\w+\s*=\s*['\"].*['\"]$", stripped):
        var, val = stripped.split("=")
        var = var.strip()
        local_vars[var] = "char*"
        return "    " * indent + f"char {var}[100] = {val.strip()};"

    # List assignment (e.g., arr = [1, 2, 3, 4] or arr = [1.0, 2.0])
    if re.match(r"^\w+\s*=\s*\[.*\]$", stripped):
        var, val = stripped.split("=")
        var = var.strip()
        val = val.strip()[1:-1]  # Remove [ and ]
        elements = [e.strip() for e in val.split(",") if e.strip()]
        if not elements:
            local_vars[var] = "int[]"
            return "    " * indent + f"int {var}[] = {{}};"
        # Determine type based on first element
        first_element = elements[0]
        if re.match(r"^\d+\.\d+$", first_element):
            type_name = "float"
        elif re.match(r"^\d+$", first_element):
            type_name = "int"
        elif re.match(r"^['\"].*['\"]$", first_element):
            type_name = "char*"
        else:
            type_name = "int"  # Default fallback
        local_vars[var] = f"{type_name}[]"
        return "    " * indent + f"{type_name} {var}[] = {{{val}}};"

    # For loop
    if stripped.startswith("for") and "range" in stripped:
        var = re.search(r"for\s+(\w+)\s+in", stripped).group(1)
        range_args = re.search(r"range\(([^)]+)\)", stripped).group(1).split(",")
        if len(range_args) == 1:
            start, end, step = 0, range_args[0].strip(), 1
        elif len(range_args) == 2:
            start, end = range_args[0].strip(), range_args[1].strip()
            step = 1
        else:
            start, end, step = range_args[0].strip(), range_args[1].strip(), range_args[2].strip()
        local_vars[var] = "int"
        return "    " * indent + f"for (int {var} = {start}; {var} < {end}; {var} += {step}) {{"

    # If statement
    if stripped.startswith("if"):
        condition = stripped[2:].strip().rstrip(":")
        condition = condition.replace(" and ", " && ").replace(" or ", " || ")
        return "    " * indent + f"if ({condition}) {{"

    # Elif statement
    if stripped.startswith("elif"):
        condition = stripped[4:].strip().rstrip(":")
        condition = condition.replace(" and ", " && ").replace(" or ", " || ")
        return "    " * indent + f"else if ({condition}) {{"

    # Else statement
    if stripped == "else:":
        return "    " * indent + "else {"

    # While loop
    if stripped.startswith("while"):
        condition = stripped[5:].strip().rstrip(":")
        condition = condition.replace(" and ", " && ").replace(" or ", " || ")
        return "    " * indent + f"while ({condition}) {{"

    # Handle math.something function calls
    if re.match(r"^math\.\w+\s*\(.*\)$", stripped):
        func_call = re.sub(r"^math\.", "", stripped)  # Remove math. prefix
        return "    " * indent + f"{func_call};"

    # Function call detection
    if re.match(r"^\w+\s*\(.*\)$", stripped) and not stripped.startswith(("def ", "print(", "int(", "float(", "input(")):
        return "    " * indent + f"{stripped};"

    # General assignment (e.g., res = a + b or res = math.something(x))
    if re.match(r"^\w+\s*=\s*.+$", stripped):
        var, expr = map(str.strip, stripped.split("=", 1))
        expr = expr.replace(" and ", " && ").replace(" or ", " || ")

        # Handle math.something in assignments
        if re.match(r"^math\.\w+\s*\(.*\)$", expr):
            func_call = re.sub(r"^math\.", "", expr)  # Remove math. prefix
            local_vars[var] = "int"  # Default to int for math functions
            return "    " * indent + f"int {var} = {func_call};"

        # Infer type from expression
        inferred_type = "int"  # default
        if re.match(r"^\d+\.\d+$", expr):
            inferred_type = "float"
        elif re.match(r"^\d+$", expr):
            inferred_type = "int"
        elif re.match(r"^['\"].*['\"]$", expr):
            inferred_type = "char*"
        elif re.match(r"^\w+\s*[\+\-\*/]\s*\w+$", expr):  # a + b
            tokens = re.split(r"[\+\-\*/]", expr)
            types = {local_vars.get(tok.strip(), "int") for tok in tokens}
            if "char*" in types:
                inferred_type = "char*"
            elif "float" in types:
                inferred_type = "float"
            elif "int" in types:
                inferred_type = "int"
        elif expr in local_vars:
            inferred_type = local_vars[expr]

        local_vars[var] = inferred_type
        return "    " * indent + f"{inferred_type} {var} = {expr};"

    # Fallback
    return "    " * indent + "// " + stripped

def convert_file(input_file, output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    # Initialize output with standard C includes
    output = [
        "#include <stdio.h>",
        "#include <string.h>",
    ]

    # Dictionary to map Python libraries to C includes
    library_map = {
        "math": "#include <math.h>",
    }

    # Process imports and add corresponding C includes
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import"):
            lib_name = stripped.split()[1]
            if lib_name in library_map:
                output.append(library_map[lib_name])
            continue
        break  # Stop processing imports after the first non-import line

    output.append("")  # Add a blank line after includes

    func_code = []
    main_code = ["int main() {"]
    block_indents = [0]
    func_block_indents = []
    curr_func_indent = None
    curr_func_name = None
    return_types = {}
    func_defs = []
    last_indent = 0
    local_vars = {}

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import"):
            continue
        indent = (len(line) - len(line.lstrip())) // 4 if stripped else last_indent

        while block_indents and indent < block_indents[-1]:
            block_indents.pop()
            main_code.append("    " * indent + "}")

        if curr_func_indent is not None and stripped:
            while func_block_indents and indent < func_block_indents[-1]:
                func_block_indents.pop()
                func_code.append("    " * indent + "}")
            if indent <= curr_func_indent:
                func_code.append("    " * curr_func_indent + "}")
                return_type = "void"
                if curr_func_name in return_types:
                    types = return_types[curr_func_name]
                    if len(types) == 1:
                        return_type = types.pop()
                    elif "float" in types:
                        return_type = "float"
                    elif "int" in types:
                        return_type = "int"
                    elif "char*" in types:
                        return_type = "char*"
                for fdef in func_defs:
                    if fdef["name"] == curr_func_name:
                        fdef["final_line"] = fdef["line"].replace("_RETURN_TYPE_", return_type)
                curr_func_indent = None
                curr_func_name = None
                local_vars = {}

        if not stripped:
            continue
        last_indent = indent

        if stripped.startswith("def "):
            curr_func_indent = indent
            curr_func_name = stripped.split("(")[0].replace("def ", "").strip()
            return_types[curr_func_name] = set()
            local_vars = {}
            translated = translate_line(line, indent, True, curr_func_name, return_types, local_vars)
            func_defs.append(translated)
            func_code.append(translated["line"])
            continue

        translated = translate_line(line, indent, curr_func_indent is not None, curr_func_name, return_types, local_vars)
        target = func_code if curr_func_indent is not None else main_code
        if isinstance(translated, list):
            target.extend(translated)
        else:
            target.append(translated)

        if isinstance(translated, str) and translated.endswith("{"):
            if curr_func_indent is not None:
                func_block_indents.append(indent + 1)
            else:
                block_indents.append(indent + 1)

    if curr_func_indent is not None:
        while func_block_indents:
            indent = func_block_indents.pop()
            func_code.append("    " * (indent - 1) + "}")
        func_code.append("    " * curr_func_indent + "}")
        return_type = "void"
        if curr_func_name in return_types:
            types = return_types[curr_func_name]
            if len(types) == 1:
                return_type = types.pop()
            elif "float" in types:
                return_type = "float"
            elif "int" in types:
                return_type = "int"
            elif "char*" in types:
                return_type = "char*"
        for fdef in func_defs:
            if fdef["name"] == curr_func_name:
                fdef["final_line"] = fdef["line"].replace("_RETURN_TYPE_", return_type)

    while len(block_indents) > 1:
        indent = block_indents.pop()
        main_code.append("    " * (indent - 1) + "}")

    main_code.append("    return 0;")
    main_code.append("}")

    final_func_code = []
    for line in func_code:
        if "_RETURN_TYPE_" in line:
            for fdef in func_defs:
                if fdef["line"] == line:
                    final_func_code.append(fdef["final_line"])
                    break
        else:
            final_func_code.append(line)

    output.extend(final_func_code)
    output.append("")
    output.extend(main_code)

    with open(output_file, "w") as f:
        f.write("\n".join(output))

    print(f"✅ Converted to {output_file}")

if __name__ == "__main__":
    convert_file("input.py", "output.c")