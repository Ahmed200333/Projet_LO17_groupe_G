import re
import html
from pathlib import Path
from itertools import zip_longest


DATA_PATH = Path("../data")
    
# Extrait la date
def extractDate(text):
    match = re.search(r"\d{4}/\d{2}/\d{2}",text, re.IGNORECASE)
    date = match.group()
    date = date.split("/")
    new_date = date[2] + "/" + date[1] + "/" + date[0]
    if match:
        return new_date

# Extrait la rubrique
def extractRubrique(text):
    match = re.search(r"<p class=.style96.><span class=.style42.>(.*?)<br></span>", text, re.IGNORECASE)
    if match:
        return html.unescape(match.group(1))
    
# Extrait le titre
def extractTitle(text):
    match = re.search(r"<title>(.*?)&gt;(.*?)&gt; (.*?)</title>", text, re.IGNORECASE)
    if match:
        return html.unescape(match.group(3))

# Extrait le numéro du bulletin
def extractNumeroBulletin(text):
    match = re.search(r"'Numero', '(.*?(\d{3,4}))'",text, re.IGNORECASE)
    if match:
        return html.unescape(match.group(2))

# Extrait le numéro de l'article
def extractNumeroArticle(text):
    match = re.search(r"'Code', '(.*?(\d{4,5}))'",text, re.IGNORECASE)
    if match:
        return html.unescape(match.group(2))

# Extrait l'auteur
def extractAuteur(text):
    match = re.search(r"<span class=.style95.>(.*?)\s*-\s*(.*?)\s*-\s*emai", text, re.IGNORECASE)
    if match:
        return html.unescape(match.group(2))

# Extrait le texte de l'article
def extractTexte(text):
    matches = re.findall(r'<p class="style96"><span class="style95">(.*?)</span></p>', text, re.DOTALL)
    if matches:
        text = ' '.join(matches).strip()
        text = re.sub(r'<[^>]+>', '', text)
        text = ' '.join(text.split())
        return html.unescape(text)
    return None

# Extrait les images
def extractImages(text):
    matches = re.findall(r'<img src="(.*?\.jpg)"', text, re.IGNORECASE)
    return [html.unescape(url) for url in matches]

# Extrait la légende
def extractLegende(text):
    matches = re.findall(r'<span class="style88">(.*?)</span></div><span class="style95"><br />', text, re.IGNORECASE)
    return [html.unescape(legende) for legende in matches]

# Extrait les contacts
def extractContact(text):
    match = re.search(r'<p class="style44"><span class="style85">(.*?)</span>', text, re.IGNORECASE)
    if match:
        text = re.sub(r'<[^>]+>', '', match.group(1))
        return html.unescape(text)

# Rédige le corpus à partir des fichiers HTML grâce aux fonctions d'extraction ci-dessus
def main():
    with open("corpus.xml", "w", encoding="utf-8") as xml:
        xml.write("<corpus>\n")
        for file in DATA_PATH.glob("*.htm"):
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                xml.write("\t<document>\n")
                xml.write(f"\t\t<article>{extractNumeroArticle(content)}</article>\n")
                xml.write(f"\t\t<bulletin>{extractNumeroBulletin(content)}</bulletin>\n")
                xml.write(f"\t\t<date>{extractDate(content)}</date>\n")
                xml.write(f"\t\t<rubrique>{extractRubrique(content)}</rubrique>\n")
                xml.write(f"\t\t<titre>{extractTitle(content)}</titre>\n")
                xml.write(f"\t\t<auteur>{extractAuteur(content)}</auteur>\n")
                xml.write(f"\t\t<texte>{extractTexte(content)}</texte>\n")
                images = extractImages(content)
                legendes = extractLegende(content)
                xml.write(f"\t\t<images>\n")
                for url, legende in zip_longest(images, legendes, fillvalue=""):
                    xml.write(f"\t\t\t<image>\n")
                    xml.write(f"\t\t\t\t<urlImage>{url}</urlImage>\n")
                    xml.write(f"\t\t\t\t<legendeImage>{legende}</legendeImage>\n")
                    xml.write(f"\t\t\t</image>\n")
                xml.write(f"\t\t</images>\n")
                xml.write(f"\t\t<contact>{extractContact(content)}</contact>\n")
                xml.write("\t</document>\n")
        xml.write("</corpus>\n")

if __name__ == "__main__":
    main()