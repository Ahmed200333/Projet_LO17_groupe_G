import re
from pathlib import Path

"""
— le numéro de l'article,
— le numéro du bulletin,
— la date ---> ok,
— la rubrique,
— le titre de l'article,
— l'auteur de l'article,
— le texte de l'article,
— la ou les images avec leur(s) URL(s) et leur(s) légende(s) respective(s),
— les informations de contact.
"""

DATA_PATH = Path("../data")
    
# Fonctionnel (testé pour tous les fichiers)
def extractDate(text):
    match = re.search(r"\d{4}/\d{2}/\d{2}",text)
    if match:
        return match.group()

def main():
    for file in DATA_PATH.glob("*.htm"):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            date = extractDate(content)
            print(f"file: {file.name} --> {date}")
    

if __name__ == "__main__":
    main()