from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import ssl
import requests

#Zeilen mit bestimmten Wörtern entfernen
def remove_triggerword_lines(text, woerterliste):
    # Teile den Text in Zeilen auf
    zeilen = text.split('\n')
    
    # Verwende eine Liste, um die Zeilen zu speichern, die nicht die bestimmten Wörter enthalten
    bereinigte_zeilen = [zeile for zeile in zeilen if not any(wo in zeile for wo in woerterliste)]
    
    # Füge die bereinigten Zeilen wieder zu einem Text zusammen
    bereinigter_text = '\n'.join(bereinigte_zeilen)
    
    return bereinigter_text

# Definiere den URL, den du abrufen möchtest
url = "https://alkiskurul.com/"

#Triggerwörter (siehe definierte Funktion oben)
triggerwoerterliste = ["Terms", "Policy", "Donate", "Store", "License"]

# Erstelle ein SSL-Kontext-Objekt, das benutzerdefinierte Zertifikatsstellen zulässt
ssl_context = ssl.create_default_context()

#Enable OP_LEGACY_SERVER_CONNECT
ssl_context.options |= 0x4

# Verwende das SSL-Kontext-Objekt, um die Verbindung mit der Website herzustellen
html = urlopen(url, context=ssl_context)

soup = BeautifulSoup(html, features="html.parser")

for script in soup(["script", "style"]):
    script.extract()

text = soup.get_text()


#Einwortzeilen entfernen
EWZT = input("Zeilen mit nur einem Wort entfernen? [y/n]")

if EWZT == "y":
    text = re.sub(r'^\s*\w+\s*$', '', text, flags=re.MULTILINE)

#Nichtlateinische Zeilen entfernen
NLZT = input("Zeilen mit nicht-lateinischen Zeichen entfernen? [y/n] (nicht empfohlen)")

if NLZT == "y":
    text = re.sub(r'^(?=.*[^\u0000-\u007F]).*$', '', text, flags=re.MULTILINE)

#Triggerwörterzeilen entfernen
TWLT = input("Triggerwortliste benutzen? [y/n] (Alle Zeilen, die Wörter aus der Liste enthalten, werden entfernt)")

if TWLT == "y":
    text = remove_triggerword_lines(text, triggerwoerterliste)

#Leere Zeilen entfernen
text = re.sub(r'\n\s*\n', '\n', text)

print("----------------\n" + text)
