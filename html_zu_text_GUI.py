import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter import filedialog
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import ssl
import requests

def remove_triggerword_lines(text, woerterliste):
    # Teile den Text in Zeilen auf
    zeilen = text.split('\n')
    
    # Verwende eine Liste, um die Zeilen zu speichern, die nicht die bestimmten Wörter enthalten
    bereinigte_zeilen = [zeile for zeile in zeilen if not any(wo in zeile for wo in woerterliste)]
    
    # Füge die bereinigten Zeilen wieder zu einem Text zusammen
    bereinigter_text = '\n'.join(bereinigte_zeilen)
    
    return bereinigter_text

ssl_context = ssl.create_default_context()
ssl_context.options |= 0x4

# Erstellen des Hauptfensters
root = tk.Tk()
root.title("HTML zu Text GUI")

trigger_words = ["Terms", "Policy", "Donate", "Store", "License", "E-Mail", "Cookies", "Login", "Register"]

# Das Hauptfenster zentrieren und eine feste Größe festlegen
window_width = 600
window_height = 800  # Erhöht, um Platz für die zusätzlichen Fragen zu schaffen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Frame zur Zentrierung der Inhalte
frame = tk.Frame(root)
frame.pack(expand=True)

# URL Label und Eingabefeld
url_label = tk.Label(frame, text="URL")
url_label.pack()

url_entry = tk.Entry(frame, width=60)
url_entry.pack()

space_frame = tk.Frame(frame, height=10)
space_frame.pack()

question_label = tk.Label(frame, text="Zeilen mit nur einem Wort entfernen?")
question_label.pack()

answer = tk.IntVar()
yes_radiobutton = tk.Radiobutton(frame, text="Ja", variable=answer, value=1)
yes_radiobutton.pack()

no_radiobutton = tk.Radiobutton(frame, text="Nein", variable=answer, value=2)
no_radiobutton.pack()

space_frame = tk.Frame(frame, height=10)
space_frame.pack()

question_label_2 = tk.Label(frame, text="Zeilen mit nicht-lateinischen Zeichen entfernen? (nicht empfohlen)")
question_label_2.pack()

answer_2 = tk.IntVar()
answer_2.set(2)  # Voreinstellung auf 2 setzen
yes_radiobutton_2 = tk.Radiobutton(frame, text="Ja", variable=answer_2, value=1)
yes_radiobutton_2.pack()

no_radiobutton_2 = tk.Radiobutton(frame, text="Nein", variable=answer_2, value=2)
no_radiobutton_2.pack()

space_frame = tk.Frame(frame, height=10)
space_frame.pack()

question_label_3 = tk.Label(frame, text="Triggerwortliste benutzen? (Alle Zeilen, die Wörter aus der Liste enthalten, werden entfernt)")
question_label_3.pack()

answer_3 = tk.IntVar()
yes_radiobutton_3 = tk.Radiobutton(frame, text="Ja", variable=answer_3, value=1)
yes_radiobutton_3.pack()

no_radiobutton_3 = tk.Radiobutton(frame, text="Nein", variable=answer_3, value=2)
no_radiobutton_3.pack()

# Liste für Triggerwörter
listbox = tk.Listbox(frame, selectmode=tk.SINGLE)
for word in trigger_words:
    listbox.insert(tk.END, word)
listbox.pack()

# Schaltflächen zum Hinzufügen und Entfernen von Triggerwörtern
def add_word():
    word = askstring("Hinzufügen", "Geben Sie das Triggerwort ein:")
    if word:
        listbox.insert(tk.END, word)
        trigger_words = listbox.get(0, tk.END)

def remove_word():
    selected_index = listbox.curselection()
    if selected_index:
        listbox.delete(selected_index)
        trigger_words = listbox.get(0, tk.END)

add_button = tk.Button(frame, text="Hinzufügen", command=add_word)
remove_button = tk.Button(frame, text="Entfernen", command=remove_word)
add_button.pack()
remove_button.pack()

space_frame = tk.Frame(frame, height=10)
space_frame.pack()

question_label_4 = tk.Label(frame, text="Alle leere Zeilen entfernen? (Es sind mehr leere Zeilen als \nauf der ursprünglichen Seite, da alle entfernten Zeilen leere Zeilen sind.)")
question_label_4.pack()

answer_4 = tk.IntVar()
yes_radiobutton_4 = tk.Radiobutton(frame, text="Ja", variable=answer_4, value=1)
yes_radiobutton_4.pack()

no_radiobutton_4 = tk.Radiobutton(frame, text="Nein", variable=answer_4, value=2)
no_radiobutton_4.pack()

space_frame = tk.Frame(frame, height=10)
space_frame.pack()

storage_label = tk.Label(frame, text="Speicherort: (Textdatei wählen)")
storage_label.pack()

# Pfad-Explorer-Widget
storage_path = tk.Entry(frame, width=60)
storage_path.pack()

# Schaltfläche "Durchsuchen" zum Auswählen eines Speicherorts
def browse_storage():
    folder_path = filedialog.askopenfilename()
    if folder_path:
        storage_path.delete(0, tk.END)  # Löschen des aktuellen Inhalts des Textfelds
        storage_path.insert(0, folder_path)  # Setzen des ausgewählten Pfads

browse_button = tk.Button(frame, text="Durchsuchen", command=browse_storage)
browse_button.pack()

space_frame = tk.Frame(frame, height=20)
space_frame.pack()

def run_the_magic():
    url = url_entry.get()
    
    trigger_words = listbox.get(0, tk.END)

    html = urlopen(url, context=ssl_context)

    soup = BeautifulSoup(html, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    if answer.get() == 1:
        text = re.sub(r'^\s*\w+\s*$', '', text, flags=re.MULTILINE)
    if answer_2.get() == 1:
        text = re.sub(r'^(?=.*[^\u0000-\u007F]).*$', '', text, flags=re.MULTILINE)
    if answer_3.get() == 1:
        text = remove_triggerword_lines(text, trigger_words)
    if answer_4.get() == 1:
        text = re.sub(r'\n\s*\n', '\n', text)

    print("\n" + text)

    if storage_path.get() != '':
        text_file = open(storage_path.get(), 'w')
        text_file.write(text)
        text_file.close()

# Bestätigungsbutton
confirm_button = tk.Button(frame, text="Bestätigen", command=run_the_magic)
confirm_button.pack()

# Tkinter Hauptloop starten
root.mainloop()
