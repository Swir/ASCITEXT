import tkinter as tk
from tkinter import ttk, scrolledtext
import pyfiglet
import pyperclip
import webbrowser


def generate_ascii():
    text = text_entry.get()
    font = fonts_combobox.get()
    width = int(width_entry.get()) if width_entry.get().isdigit() else 100
    alignment = align_combobox.get()

    try:
        ascii_art = pyfiglet.figlet_format(text, font=font, width=width)
        if alignment == "Center":
            ascii_art = "\n".join(line.center(width) for line in ascii_art.splitlines())
        elif alignment == "Right":
            ascii_art = "\n".join(line.rjust(width) for line in ascii_art.splitlines())
    except pyfiglet.FontNotFound:
        ascii_art = "The selected font could not be found!"

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.INSERT, ascii_art)


def copy_ascii():
    ascii_art = result_text.get(1.0, tk.END)
    pyperclip.copy(ascii_art)


def open_github():
    webbrowser.open("https://github.com/Swir")


root = tk.Tk()
root.title("Graffiti ASCII Art Generator - English")
root.geometry("860x640")
root.config(bg="#2e2e2e")

main_frame = ttk.Frame(root, padding="10", style="Main.TFrame")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
style.configure("Accent.TButton", background="#FF5722", foreground="#ffffff", font=("Arial", 10, "bold"))
style.map(
    "Accent.TButton",
    background=[("pressed", "#FF7043"), ("active", "#FF8A65")],
    foreground=[("pressed", "#ffffff"), ("active", "#ffffff")],
)

text_label = ttk.Label(main_frame, text="Enter text:")
text_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
text_entry = ttk.Entry(main_frame, width=45)
text_entry.grid(row=0, column=1, padx=5, pady=5)

font_label = ttk.Label(main_frame, text="Choose font:")
font_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

font_options = sorted(pyfiglet.FigletFont.getFonts())
fonts_combobox = ttk.Combobox(main_frame, values=font_options, width=42)
fonts_combobox.grid(row=1, column=1, padx=5, pady=5)
fonts_combobox.set(font_options[0])

width_label = ttk.Label(main_frame, text="Width (default 100):")
width_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
width_entry = ttk.Entry(main_frame, width=45)
width_entry.insert(0, "100")
width_entry.grid(row=2, column=1, padx=5, pady=5)

align_label = ttk.Label(main_frame, text="Alignment:")
align_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
align_options = ["Left", "Center", "Right"]
align_combobox = ttk.Combobox(main_frame, values=align_options, width=42)
align_combobox.grid(row=3, column=1, padx=5, pady=5)
align_combobox.set("Left")

generate_button = ttk.Button(main_frame, text="Generate ASCII Art", command=generate_ascii, style="Accent.TButton")
generate_button.grid(row=4, column=0, columnspan=2, pady=10)

copy_button = ttk.Button(main_frame, text="Copy ASCII Art", command=copy_ascii, style="Accent.TButton")
copy_button.grid(row=5, column=0, columnspan=2, pady=5)

result_text = scrolledtext.ScrolledText(main_frame, width=100, height=20, wrap=tk.NONE, bg="#3c3c3c", fg="#ffffff")
result_text.grid(row=6, column=0, columnspan=2, pady=10, padx=5)

result_text.config(xscrollcommand=result_text.xview)
result_text_scroll_x = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=result_text.xview)
result_text_scroll_x.grid(row=7, column=0, columnspan=2, sticky="ew")
result_text["xscrollcommand"] = result_text_scroll_x.set

bottom_frame = ttk.Frame(root, style="Main.TFrame")
bottom_frame.grid(row=8, column=0, pady=10, sticky="ew")

soft_label = ttk.Label(bottom_frame, text="Software by Swir", style="TLabel", font=("Arial", 10, "italic"))
soft_label.pack(side="left", padx=5)

github_button = ttk.Button(bottom_frame, text="GitHub: https://github.com/Swir", command=open_github, style="Accent.TButton")
github_button.pack(side="right", padx=5)

root.mainloop()
