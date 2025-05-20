import tkinter as tk
from tkinter import scrolledtext
import importlib.util

def run_converter(module_path, input_code, output_path):
    with open("temp_input.py", "w") as temp_file:
        temp_file.write(input_code)

    try:
        spec = importlib.util.spec_from_file_location("index", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        module.convert_file("temp_input.py", output_path)

        with open(output_path, "r") as f:
            return f.read(), True
    except Exception as e:
        return f"Error during conversion: {e}", False

def convert_code():
    input_code = input_text.get("1.0", tk.END).strip()
    if not input_code:
        status_label.config(text="⚠️ Please enter Python/C++ code!", fg="#FFA500")
        return

    lang = language_var.get()
    if lang == "Java":
        output, ok = run_converter("p2j/index.py", input_code, "p2j/converted_code.java")
    elif lang == "C++":
        output, ok = run_converter("p2c++/main.py", input_code, "p2c++/output.c++")
    elif lang == "cpptojava":
        output, ok = run_converter("cpptojava/main.py", input_code, "cpptojava/output.java")
    elif lang == "C":
        output, ok = run_converter("p2c/main.py", input_code, "p2c/output.c")
    else:
        output = "// Unknown language"
        ok = False

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)

    if ok:
        status_label.config(text="✅ Code converted successfully!", fg="#28a745")
    else:
        status_label.config(text="❌ Conversion failed!", fg="#dc3545")

# GUI Setup
root = tk.Tk()
root.title("🌈 LeetCode-Style Code Converter")
root.geometry("1200x720")
root.configure(bg="#f0f8ff")

title = tk.Label(root, text="✨ Code Converter Interface", font=("Helvetica", 22, "bold"), bg="#f0f8ff", fg="#4B0082")
title.pack(pady=15)

# Language selection
language_var = tk.StringVar(value="Java")
lang_frame = tk.Frame(root, bg="#f0f8ff")
lang_frame.pack()

tk.Label(lang_frame, text="Select Language:", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#000080").pack(side=tk.LEFT, padx=5)
tk.Radiobutton(lang_frame, text="Python to Java", variable=language_var, value="Java", bg="#f0f8ff", fg="#006400", font=("Arial", 11)).pack(side=tk.LEFT)
tk.Radiobutton(lang_frame, text="Python to C++", variable=language_var, value="C++", bg="#f0f8ff", fg="#8B0000", font=("Arial", 11)).pack(side=tk.LEFT)
tk.Radiobutton(lang_frame, text="C++ to Java", variable=language_var, value="cpptojava", bg="#f0f8ff", fg="#800080", font=("Arial", 11)).pack(side=tk.LEFT)
tk.Radiobutton(lang_frame, text="Python to C", variable=language_var, value="C", bg="#f0f8ff", fg="#0000CD", font=("Arial", 11)).pack(side=tk.LEFT)

# Two-pane layout
pane = tk.Frame(root, bg="#f0f8ff")
pane.pack(pady=10, fill=tk.BOTH, expand=True)

# Left pane - Input
input_frame = tk.Frame(pane, bg="#f0f8ff")
input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5))

tk.Label(input_frame, text="💻 Input Code", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#00008B").pack()
input_text = scrolledtext.ScrolledText(
    input_frame,
    width=60,
    height=30,
    font=("Consolas", 11),
    bg="#fffacd",
    fg="black",
    insertbackground="black"
)
input_text.pack(fill=tk.BOTH, expand=True)

# Right pane - Output
output_frame = tk.Frame(pane, bg="#f0f8ff")
output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10))

tk.Label(output_frame, text="🧾 Converted Code", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#00008B").pack()
output_text = scrolledtext.ScrolledText(
    output_frame,
    width=60,
    height=30,
    font=("Consolas", 11),
    bg="#e6f2ff",
    fg="black",
    insertbackground="black"
)
output_text.pack(fill=tk.BOTH, expand=True)

# Convert Button
tk.Button(
    root,
    text="🔄 Convert",
    font=("Arial", 12, "bold"),
    bg="#007BFF",
    fg="white",
    activebackground="#0056b3",
    padx=10,
    pady=5,
    command=convert_code
).pack(pady=15)

# Status Label
status_label = tk.Label(root, text="", font=("Arial", 11), bg="#f0f8ff")
status_label.pack()

root.mainloop()
