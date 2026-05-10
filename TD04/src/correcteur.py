import re
import spacy #type: ignore

# Extrait tous les lemmes uniques du corpus pour construire le lexique de référence
def build_lexique(corpus="../../TD03/data/corpus_lematized.xml"):
    lexique = set()
    with open(corpus, 'r', encoding="UTF-8") as file:
        content = file.read()
        for ligne in content.splitlines():
            ligne = ligne.strip()
            if ligne.startswith("<titre>") or ligne.startswith("<texte>"):
                texte = re.sub(r"<[^>]+>", "", ligne).strip()
                for lemme in texte.split():
                    lexique.add(lemme)
    with open("../data/lexique.txt","w", encoding="UTF-8") as out:
        for lemme in sorted(lexique):
            out.write(lemme + "\n")

# Charge le lexique depuis un fichier
def charger_lexique(lexique_file="../data/lexique.txt"):
    lexique = set()
    with open(lexique_file, "r", encoding="utf-8") as f:
        for ligne in f:
            mot = ligne.strip()
            if mot:
                lexique.add(mot)
    return lexique

# Tokenise une requête en mots (gère les dates JJ/MM/AAAA)
def tokeniser(requete):
    return [t.strip().lower() for t in re.findall(r"\d{1,2}/\d{1,2}/\d{4}|\w+'|[\w]+", requete, re.UNICODE) if t.strip()]

# Lemmatise chaque token via spaCy
def lemmatiser(tokens, nlp):
    resultats = []
    for token in tokens:
        lemme = nlp(token)[0].lemma_
        resultats.append((token, lemme))
    return resultats

# Vérifie si un terme contient un chiffre (terme spécifique, non corrigé)
def est_specifique(terme):
    if re.search(r"\d", terme):
        return True
    else:
        return False

# Calcule la similarité par préfixe commun entre deux mots (en %)
def recherche_prefixe(m1, m2, seuil_min, seuil_max):
    if (len(m1) < seuil_min) or (len(m2) < seuil_min):
        return 0
    else:
        if abs(len(m1) - len(m2)) > seuil_max:
            return 0
        else:
            i = 0
            while (i < min(len(m1), len(m2))) and (m1[i] == m2[i]):
                i += 1
            return (i/max(len(m1), len(m2)))*100
            
# Calcule la distance de Levenshtein entre deux mots
def distance_levenshtein(m1, m2):
    n, m = len(m1), len(m2)
    dist = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dist[i][0] = i
    for j in range(m + 1):
        dist[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if m1[i - 1] == m2[j - 1]:
                dist[i][j] = min(dist[i-1][j] + 1, dist[i][j-1] + 1, dist[i-1][j-1])
            else:
                dist[i][j] = min(dist[i-1][j] + 1, dist[i][j-1] + 1, dist[i-1][j-1] + 1)
    return dist[n][m]

# Corrige une requête : tokenise, lemmatise, puis corrige via préfixe + Levenshtein
def main(requete, lexique_path="../data/lexique.txt"):
      nlp = spacy.load("fr_core_news_sm")
      lexique = charger_lexique(lexique_path)

      tokens = tokeniser(requete)
      termes = lemmatiser(tokens, nlp)

      resultats = []
      for token, lemme in termes:
          # Les termes avec chiffres sont gardés tels quels
          if est_specifique(token):
              resultats.append(token)
              continue
          # Si le lemme existe dans le lexique, pas besoin de correction
          if lemme in lexique:
              resultats.append(lemme)
              continue
          # Sinon, recherche de candidats par similarité de préfixe
          candidats = []
          for mot_lexique in lexique:
              prox = recherche_prefixe(lemme, mot_lexique, 3, 4)
              if prox > 60:
                  candidats.append(mot_lexique)
          # Sélection du meilleur candidat par distance de Levenshtein
          if len(candidats) == 1:
              resultats.append(candidats[0])
          elif len(candidats) > 1:
              meilleur = min(candidats, key=lambda c: distance_levenshtein(lemme, c))
              resultats.append(meilleur)
          else:
              resultats.append(lemme) 

      return " ".join(resultats)


if __name__ == "__main__":
    # build_lexique()
    requete = input("Entrez votre requête : ")
    main(requete)