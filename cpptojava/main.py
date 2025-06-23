import re
import os

def translate_cpp_to_java(lines):
    java_lines = [
        "import java.util.*;",
        "public class Main {"
    ]

    indent = "    "
    var_types = {}
    func_lines = []
    main_lines = []

    in_function = False
    function_buffer = []
    brace_count = 0

    for line in lines:
        stripped = line.strip()

        if not stripped or stripped.startswith("//"):
            continue

        if "#include" in stripped or "using namespace std;" in stripped:
            continue

        func_match = re.match(r"(int|float|double|string|void)\s+(\w+)\s*\((.*)\)\s*{?", stripped)
        if func_match and not re.match(r"int\s+main\s*\(\s*(void)?\s*\)", stripped):
            in_function = True
            brace_count = 0
            function_buffer.append(stripped)
            if '{' in stripped:
                brace_count += 1
            continue

        if in_function:
            function_buffer.append(stripped)
            brace_count += stripped.count('{')
            brace_count -= stripped.count('}')
            if brace_count == 0:
                java_func_lines = convert_function(function_buffer)
                func_lines.extend(java_func_lines)
                function_buffer = []
                in_function = False
            continue

        if re.match(r"int\s+main\s*\(\s*(void)?\s*\)", stripped):
            main_lines.append(f"{indent}public static void main(String[] args) "+"{")
            main_lines.append(f"{indent*2}Scanner sc = new Scanner(System.in);")
            continue

        if stripped == "return 0;" or stripped == "return 0":
            main_lines.append(f"{indent}}}")
            continue

        if main_lines:
            if match := re.match(r"(int|float|double|string)\s+(\w+)\[(\d+)?\];", stripped):
                t, name, size = match.groups()
                t_java = "String" if t == "string" else t
                size_val = size if size else "100"
                main_lines.append(f"{indent*2}{t_java}[] {name} = new {t_java}[{size_val}];")
                var_types[name] = f"{t_java}[]"
                continue

            if match := re.match(r"(int|float|double|string)\s+([\w\s,]+);", stripped):
                t = match.group(1)
                vars_str = match.group(2)
                t_java = "String" if t == "string" else t
                vars_list = [v.strip() for v in vars_str.split(",")]
                var_types.update({v: t_java for v in vars_list})
                vars_joined = ", ".join(vars_list)
                main_lines.append(f"{indent*2}{t_java} {vars_joined};")
                continue

            if match := re.match(r"(int|float|double|string)\s+(\w+)\s*=\s*(.*);", stripped):
                t, var, val = match.groups()
                t_java = "String" if t == "string" else t
                var_types[var] = t_java
                main_lines.append(f"{indent*2}{t_java} {var} = {val};")
                continue

            if "cin >>" in stripped:
                vars_ = [v.strip().replace(";", "") for v in stripped.split(">>")[1:]]
                for v in vars_:
                    base_type = var_types.get(v, "String").replace("[]", "")
                    read_method = {
                        "int": "nextInt()",
                        "float": "nextFloat()",
                        "double": "nextDouble()",
                        "String": "next()"
                    }.get(base_type, "next()")
                    main_lines.append(f"{indent*2}{v} = sc.{read_method};")
                continue

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

            if stripped.startswith("return"):
                if not stripped.endswith(";"):
                    stripped += ";"
                main_lines.append(f"{indent*2}{stripped}")
                continue

            if any(stripped.startswith(keyword) for keyword in ["if", "else if", "else", "for", "while"]):
                main_lines.append(f"{indent*2}{stripped}")
                continue

            if stripped in ["{", "}"]:
                main_lines.append(f"{indent*2}{stripped}")
                continue

            if stripped and not stripped.startswith("//"):
                if stripped.endswith(";"):
                    main_lines.append(f"{indent*2}{stripped}")
                else:
                    main_lines.append(f"{indent*2}{stripped};")
            elif stripped:
                main_lines.append(f"{indent*2}{stripped}")

    java_lines.extend(func_lines)
    java_lines.extend(main_lines)

    if not (java_lines and java_lines[-1].strip() == "}"):
        java_lines.append("}")

    return java_lines

def convert_function(func_lines):
    converted = []
    indent = "    "

    header = func_lines[0]
    m = re.match(r"(int|float|double|string|void)\s+(\w+)\s*\((.*)\)\s*{?", header)
    if not m:
        return ["// Could not parse function: " + header]

    ret_type, name, params = m.groups()
    ret_type_java = "String" if ret_type == "string" else ret_type

    param_list = []
    params = params.strip()
    if params:
        for p in params.split(","):
            p = p.strip()
            pt_match = re.match(r"(int|float|double|string)\s*(\[\])?\s+(\w+)", p)
            if pt_match:
                pt, is_array, pv = pt_match.groups()
                pt_java = "String" if pt == "string" else pt
                if is_array:
                    pt_java += "[]"
                param_list.append(f"{pt_java} {pv}")
            else:
                param_list.append(p)
    params_java = ", ".join(param_list)

    converted.append(f"{indent}public static {ret_type_java} {name}({params_java}) "+"{")

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
    convert_file("cpptojava/input.cpp", "cpptojava/output.java")
