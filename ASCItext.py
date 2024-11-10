import tkinter as tk
from tkinter import ttk, scrolledtext
import pyfiglet
import pyperclip
import webbrowser  # Do otwierania linków w przeglądarce

# Funkcja do generowania ASCII Art z dodatkowymi opcjami
def generuj_ascii():
    tekst = text_entry.get()  # Pobranie tekstu od użytkownika
    styl = wzory_combobox.get()  # Pobranie wybranego stylu czcionki (wzorów)
    szerokosc = int(width_entry.get()) if width_entry.get().isdigit() else 100  # Pobranie szerokości
    wyrownanie = align_combobox.get()  # Pobranie wyrównania tekstu

    try:
        # Generowanie napisu z wybraną szerokością i stylem
        ascii_art = pyfiglet.figlet_format(tekst, font=styl, width=szerokosc)
        # Zastosowanie wyrównania
        if wyrownanie == "Centrum":
            ascii_art = "\n".join(line.center(szerokosc) for line in ascii_art.splitlines())
        elif wyrownanie == "Prawo":
            ascii_art = "\n".join(line.rjust(szerokosc) for line in ascii_art.splitlines())
    except pyfiglet.FontNotFound:
        ascii_art = "Nie znaleziono wybranego stylu!"
    
    # Wyświetlanie wyniku
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.INSERT, ascii_art)

# Funkcja do kopiowania wyniku do schowka
def kopiuj_ascii():
    ascii_art = result_text.get(1.0, tk.END)  # Pobranie tekstu z pola wyników
    pyperclip.copy(ascii_art)  # Kopiowanie do schowka

# Funkcja otwierająca link do GitHub w przeglądarce
def otworz_github():
    webbrowser.open("https://github.com/Swir")

# Tworzenie głównego okna
root = tk.Tk()
root.title("Graffiti ASCII Art Generator")
root.geometry("860x640")
root.config(bg="#2e2e2e")  # Ciemne tło

# Tworzenie interfejsu z ciemnym motywem
main_frame = ttk.Frame(root, padding="10", style="Main.TFrame")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Dodanie stylu dla ciemnego motywu
style = ttk.Style(root)
style.theme_use("clam")  # Używamy motywu "clam" dla lepszego wyglądu przycisków
style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
style.configure("Accent.TButton", background="#FF5722", foreground="#ffffff", font=("Arial", 10, "bold"))
style.map(
    "Accent.TButton",
    background=[("pressed", "#FF7043"), ("active", "#FF8A65")],  # Efekt przyciskania i aktywacji
    foreground=[("pressed", "#ffffff"), ("active", "#ffffff")],
)

# Etykieta i pole tekstowe dla wprowadzenia tekstu
text_label = ttk.Label(main_frame, text="Podaj tekst:")
text_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
text_entry = ttk.Entry(main_frame, width=45)
text_entry.grid(row=0, column=1, padx=5, pady=5)

# Etykieta i lista rozwijana dla wyboru stylu ASCII
znaki_label = ttk.Label(main_frame, text="Wybierz styl:")
znaki_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

# Kompleksowa lista stylów ASCII dostępnych w pyfiglet
style_options = sorted(pyfiglet.FigletFont.getFonts())  # Pobranie wszystkich dostępnych czcionek
wzory_combobox = ttk.Combobox(main_frame, values=style_options, width=42)
wzory_combobox.grid(row=1, column=1, padx=5, pady=5)
wzory_combobox.set(style_options[0])

# Etykieta i pole dla ustawienia szerokości
width_label = ttk.Label(main_frame, text="Szerokość (default 100):")
width_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
width_entry = ttk.Entry(main_frame, width=45)
width_entry.insert(0, "100")
width_entry.grid(row=2, column=1, padx=5, pady=5)

# Etykieta i lista rozwijana dla wyrównania
align_label = ttk.Label(main_frame, text="Wyrównanie:")
align_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
align_options = ["Lewo", "Centrum", "Prawo"]
align_combobox = ttk.Combobox(main_frame, values=align_options, width=42)
align_combobox.grid(row=3, column=1, padx=5, pady=5)
align_combobox.set("Lewo")

# Przyciski z wyraźnym efektem wizualnym przy kliknięciu
generuj_button = ttk.Button(main_frame, text="Generuj ASCII Art", command=generuj_ascii, style="Accent.TButton")
generuj_button.grid(row=4, column=0, columnspan=2, pady=10)

kopiuj_button = ttk.Button(main_frame, text="Skopiuj ASCII Art", command=kopiuj_ascii, style="Accent.TButton")
kopiuj_button.grid(row=5, column=0, columnspan=2, pady=5)

# Pole wyświetlania wyników
result_text = scrolledtext.ScrolledText(main_frame, width=100, height=20, wrap=tk.NONE, bg="#3c3c3c", fg="#ffffff")
result_text.grid(row=6, column=0, columnspan=2, pady=10, padx=5)

# Pasek przewijania poziomego
result_text.config(xscrollcommand=result_text.xview)
result_text_scroll_x = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=result_text.xview)
result_text_scroll_x.grid(row=7, column=0, columnspan=2, sticky="ew")
result_text["xscrollcommand"] = result_text_scroll_x.set

# Sekcja dolna - podpis i link do GitHub
bottom_frame = ttk.Frame(root, style="Main.TFrame")
bottom_frame.grid(row=8, column=0, pady=10, sticky="ew")

soft_label = ttk.Label(bottom_frame, text="Soft by Swir", style="TLabel", font=("Arial", 10, "italic"))
soft_label.pack(side="left", padx=5)

github_button = ttk.Button(bottom_frame, text="GitHub: https://github.com/Swir", command=otworz_github, style="Accent.TButton")
github_button.pack(side="right", padx=5)

# Uruchomienie aplikacji
root.mainloop()
