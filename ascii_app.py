"""Shared, bounded ASCII rendering and PL/EN desktop interface."""
from functools import lru_cache
import json
from pathlib import Path
import re
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext
import webbrowser
import pyfiglet

VERSION = "1.1.0"
TEXT = {
    "pl": {"title":"Generator ASCII", "text":"Tekst:", "font":"Czcionka:", "width":"Szerokość (10–500):", "align":"Wyrównanie:", "aligns":["Lewo","Centrum","Prawo"], "generate":"Generuj ASCII", "copy":"Kopiuj wynik", "copied":"Skopiowano wynik.", "empty":"Wpisz tekst (maksymalnie 500 znaków).", "width_error":"Szerokość musi być liczbą całkowitą od 10 do 500.", "font_error":"Wybierz dostępną czcionkę.", "alignment_error":"Wybierz poprawne wyrównanie.", "render_error":"Nie można wyrenderować tekstu. Wybierz inną czcionkę lub większą szerokość.", "clipboard_error":"Schowek jest niedostępny. Spróbuj ponownie.", "no_result":"Najpierw wygeneruj napis."},
    "en": {"title":"ASCII Art Generator", "text":"Text:", "font":"Font:", "width":"Width (10–500):", "align":"Alignment:", "aligns":["Left","Center","Right"], "generate":"Generate ASCII", "copy":"Copy result", "copied":"Result copied.", "empty":"Enter text (up to 500 characters).", "width_error":"Width must be a whole number from 10 to 500.", "font_error":"Choose an available font.", "alignment_error":"Choose a valid alignment.", "render_error":"Cannot render this text. Choose another font or a wider output.", "clipboard_error":"The clipboard is unavailable. Please try again.", "no_result":"Generate a result first."},
}


class InputError(ValueError):
    pass


@lru_cache(maxsize=1)
def available_fonts():
    return tuple(sorted(pyfiglet.FigletFont.getFonts()))


def render_ascii(text, font, width_text="100", alignment="left"):
    if not text.strip() or len(text) > 500:
        raise InputError("empty")
    value = str(width_text).strip()
    if not re.fullmatch(r"[0-9]{1,3}", value) or not 10 <= int(value) <= 500:
        raise InputError("width_error")
    if font not in available_fonts():
        raise InputError("font_error")
    if alignment not in ("left", "center", "right"):
        raise InputError("alignment_error")
    try:
        result = pyfiglet.figlet_format(text, font=font, width=int(value), justify=alignment)
    except (pyfiglet.FigletError, ValueError, IndexError, OSError) as error:
        raise InputError("render_error") from error
    if not result.strip():
        raise InputError("render_error")
    return result


class AsciiApp:
    def __init__(self, root, language="pl"):
        self.root = root
        self.words = TEXT[language]
        root.title(f"{self.words['title']} {VERSION} — Swir")
        root.geometry("860x640")
        root.minsize(580, 420)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("App.TFrame", background="#2e2e2e")
        style.configure("App.TLabel", background="#2e2e2e", foreground="#ffffff")
        root.configure(bg="#2e2e2e")
        frame = ttk.Frame(root, padding=14, style="App.TFrame")
        frame.grid(sticky="nsew")
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(6, weight=1)
        self.text = tk.StringVar(root)
        self.font = tk.StringVar(root, "standard" if "standard" in available_fonts() else available_fonts()[0])
        self.width = tk.StringVar(root, "100")
        self.alignment = tk.StringVar(root, self.words["aligns"][0])
        self.status = tk.StringVar(root)
        controls = [ttk.Entry(frame, textvariable=self.text),
                    ttk.Combobox(frame, textvariable=self.font, values=available_fonts(), state="readonly"),
                    ttk.Entry(frame, textvariable=self.width),
                    ttk.Combobox(frame, textvariable=self.alignment, values=self.words["aligns"], state="readonly")]
        for row, (key, widget) in enumerate(zip(("text", "font", "width", "align"), controls)):
            ttk.Label(frame, text=self.words[key], style="App.TLabel").grid(row=row, column=0, sticky="w", padx=(0, 12), pady=5)
            widget.grid(row=row, column=1, sticky="ew", pady=5)
        buttons = ttk.Frame(frame, style="App.TFrame")
        buttons.grid(row=4, column=0, columnspan=2, pady=10)
        self.generate_button = ttk.Button(buttons, text=self.words["generate"], command=self.generate)
        self.generate_button.pack(side="left", padx=6)
        ttk.Button(buttons, text=self.words["copy"], command=self.copy).pack(side="left", padx=6)
        ttk.Label(frame, textvariable=self.status, style="App.TLabel", wraplength=700).grid(row=5, column=0, columnspan=2, sticky="w")
        self.output = scrolledtext.ScrolledText(frame, wrap="none", font=("Consolas", 10), bg="#252525", fg="#ffffff", insertbackground="#ffffff", state="disabled")
        self.output.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=(8, 0))
        horizontal = ttk.Scrollbar(frame, orient="horizontal", command=self.output.xview)
        horizontal.grid(row=7, column=0, columnspan=2, sticky="ew")
        self.output.configure(xscrollcommand=horizontal.set)
        ttk.Button(frame, text="GitHub · Swir", command=lambda: webbrowser.open("https://github.com/Swir")).grid(row=8, column=1, sticky="e", pady=(8, 0))
        root.bind("<Return>", lambda _event: self.generate())

    def set_output(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.configure(state="disabled")

    def generate(self):
        try:
            index = self.words["aligns"].index(self.alignment.get())
            result = render_ascii(self.text.get(), self.font.get(), self.width.get(), ("left", "center", "right")[index])
        except (InputError, ValueError) as error:
            self.status.set(self.words.get(str(error), self.words["alignment_error"]))
            self.set_output("")
            return False
        self.set_output(result)
        self.status.set("")
        return True

    def copy(self):
        result = self.output.get("1.0", "end-1c")
        if not result.strip():
            self.status.set(self.words["no_result"])
            return False
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
        except tk.TclError:
            self.status.set(self.words["clipboard_error"])
            return False
        self.status.set(self.words["copied"])
        return True


def self_test(report, language):
    root = None
    result = {"application":"ASCITEXT", "language":language, "version":VERSION, "passed":False}
    try:
        root = tk.Tk()
        root.withdraw()
        app = AsciiApp(root, language)
        root.update_idletasks()
        app.text.set("SWIR")
        app.generate_button.invoke()
        assert app.output.get("1.0", "end-1c") == render_ascii("SWIR", "standard")
        for index, alignment in enumerate(("left", "center", "right")):
            app.alignment.set(app.words["aligns"][index])
            assert app.generate()
            assert app.output.get("1.0", "end-1c") == render_ascii("SWIR", "standard", "100", alignment)
        app.width.set("0")
        assert not app.generate() and app.status.get() and not app.output.get("1.0", "end-1c")
        result.update(passed=True, checks=["Tk widgets", "bundled fonts", "render button", "three alignments", "invalid width"])
    except Exception as error:
        result["error"] = f"{type(error).__name__}: {error}"
    finally:
        if root is not None:
            root.destroy()
        Path(report).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if result["passed"] else 1


def main(language="pl"):
    if len(sys.argv) == 3 and sys.argv[1] == "--self-test":
        return self_test(sys.argv[2], language)
    root = tk.Tk()
    AsciiApp(root, language)
    root.mainloop()
    return 0
