import spacy #type: ignor
import re

def applySpacy(text):
    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    return lemmas


if __name__ == "__main__":
    with open("../../data/corpus_filtered.xml", 'r', encoding='utf-8') as file:
        content = file.read()
        for ligne in content.splitlines():
            if ligne.strip().startswith("<titre>") or ligne.strip().startswith("<texte>"):
                cleared_ligne = re.sub(r'<[^>]+>', '', ligne)
                lemmas = applySpacy(cleared_ligne)
                print(lemmas)
