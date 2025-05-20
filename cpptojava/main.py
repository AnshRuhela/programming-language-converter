import re
import os

def translate_cpp_to_java(lines):
    java_lines = [
        "import java.util.*;",
        "public class Main {"
    ]

    indent = "    "
    var_types = {}
    func_lines = []     # To store function definitions
    main_lines = []     # To store main method lines

    in_function = False
    function_buffer = []
    brace_count = 0
    current_func_signature = ""

    for line in lines:
        stripped = line.strip()

        # Skip includes and using namespace
        if "#include" in stripped or "using namespace std;" in stripped:
            continue

        # Detect function signature (not main)
        func_match = re.match(r"(int|float|double|string|void)\s+(\w+)\s*\(([^)]*)\)\s*{?", stripped)
        if func_match and not re.match(r"int\s+main\s*\(\s*(void)?\s*\)", stripped):
            in_function = True
            brace_count = 0
            current_func_signature = stripped
            function_buffer.append(stripped)
            if '{' in stripped:
                brace_count += 1
            continue

        if in_function:
            function_buffer.append(stripped)
            brace_count += stripped.count('{')
            brace_count -= stripped.count('}')
            if brace_count == 0:
                # End of function
                java_func_lines = convert_function(function_buffer)
                func_lines.extend(java_func_lines)
                function_buffer = []
                in_function = False
            continue

        # Handle main function start
        if re.match(r"int\s+main\s*\(\s*(void)?\s*\)", stripped):
            main_lines.append(f"{indent}public static void main(String[] args) "+"{")
            main_lines.append(f"{indent*2}Scanner sc = new Scanner(System.in);")
            continue

        # Handle main function end
        if stripped == "return 0;" or stripped == "return 0":
            # Close main method
            main_lines.append(f"{indent}}}")
            continue

        # Inside main body - parse other lines
        if main_lines:
            # Multiple variable declarations (e.g. int x, y;)
            if match := re.match(r"(int|float|double|string)\s+([\w\s,]+);", stripped):
                t = match.group(1)
                vars_str = match.group(2)
                t_java = "String" if t == "string" else t
                vars_list = [v.strip() for v in vars_str.split(",")]
                var_types.update({v: t_java for v in vars_list})
                vars_joined = ", ".join(vars_list)
                main_lines.append(f"{indent*2}{t_java} {vars_joined};")
                continue

            # Variable initialization (single var)
            if match := re.match(r"(int|float|double|string)\s+(\w+)\s*=\s*(.*);", stripped):
                t, var, val = match.groups()
                t_java = "String" if t == "string" else t
                var_types[var] = t_java
                main_lines.append(f"{indent*2}{t_java} {var} = {val};")
                continue

            # cin >>
            if "cin >>" in stripped:
                vars_ = [v.strip().replace(";", "") for v in stripped.split(">>")[1:]]
                for v in vars_:
                    t = var_types.get(v, "String")
                    read_method = {
                        "int": "nextInt()",
                        "float": "nextFloat()",
                        "double": "nextDouble()",
                        "String": "next()"
                    }.get(t, "next()")
                    main_lines.append(f"{indent*2}{v} = sc.{read_method};")
                continue

            # cout <<
            if "cout <<" in stripped:
                content = stripped.split("<<")[1:]
                parts = []
                for c in content:
                    c = c.strip().replace("endl", '"\\n"').rstrip(';')
                    if c.startswith('"') and c.endswith('"'):
                        parts.append(c)
                    else:
                        parts.append(f'String.valueOf({c})')
                main_lines.append(f'{indent*2}System.out.print(' + " + ".join(parts) + ');')
                continue

            # return statements
            if stripped.startswith("return"):
                main_lines.append(f"{indent*2}{stripped};")
                continue

            # Blocks and conditionals
            if any(stripped.startswith(keyword) for keyword in ["if", "else if", "else", "for", "while"]):
                # Convert conditions to Java style
                cond_line = stripped
                cond_line = cond_line.replace("&&", "&&").replace("||", "||")
                main_lines.append(f"{indent*2}{cond_line}")
                continue
            if stripped in ["{", "}"]:
                main_lines.append(f"{indent*2}{stripped}")
                continue

            # Other lines fallback
            if stripped and not stripped.startswith("//"):
                if stripped.endswith(";"):
                    main_lines.append(f"{indent*2}{stripped}")
                else:
                    main_lines.append(f"{indent*2}{stripped};")
            elif stripped:
                main_lines.append(f"{indent*2}{stripped}")

    # Close class after main and functions
    java_lines.extend(func_lines)
    java_lines.extend(main_lines)
    java_lines.append("}")

    return java_lines

def convert_function(func_lines):
    """Convert a C++ function to Java static method."""
    converted = []
    indent = "    "

    header = func_lines[0]
    # Parse function signature
    m = re.match(r"(int|float|double|string|void)\s+(\w+)\s*\(([^)]*)\)\s*{?", header)
    if not m:
        return ["// Could not parse function: " + header]

    ret_type, name, params = m.groups()
    ret_type_java = "String" if ret_type == "string" else ret_type

    # Convert params
    params = params.strip()
    if params:
        param_list = []
        for p in params.split(","):
            p = p.strip()
            pt_match = re.match(r"(int|float|double|string)\s+(\w+)", p)
            if pt_match:
                pt, pv = pt_match.groups()
                pt_java = "String" if pt == "string" else pt
                param_list.append(f"{pt_java} {pv}")
            else:
                param_list.append(p)  # fallback
        params_java = ", ".join(param_list)
    else:
        params_java = ""

    # Function header line
    converted.append(f"{indent}public static {ret_type_java} {name}({params_java}) "+"{")

    # Convert function body lines (skip signature)
    for line in func_lines[1:]:
        stripped = line.strip()
        if stripped == "}":
            converted.append(f"{indent}}}")
        elif stripped.startswith("return") and not stripped.endswith(";"):
            converted.append(f"{indent*2}{stripped};")
        else:
            if stripped and not stripped.startswith("//"):
                if stripped.endswith(";"):
                    converted.append(f"{indent*2}{stripped}")
                else:
                    converted.append(f"{indent*2}{stripped};")
            else:
                converted.append(f"{indent*2}{stripped}")

    return converted

def convert_file(input_file, output_file):
    """Interface function expected by the GUI"""
    try:
        with open(input_file, "r") as f:
            cpp_lines = f.readlines()

        java_code = translate_cpp_to_java(cpp_lines)

        with open(output_file, "w") as f:
            f.write("\n".join(java_code))

        return True
    except Exception as e:
        print(f"Conversion failed: {str(e)}")
        return False

if __name__ == "__main__":
    # For standalone testing
    convert_file("cpptojava\input.cpp", "cpptojava\output.java")