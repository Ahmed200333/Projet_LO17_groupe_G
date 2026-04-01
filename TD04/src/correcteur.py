import re
import spacy #type: ignore

def charger_lexique(lemmas_file="../data/lexique_test.txt"):
    mot_to_lemme = {}
    lemmes_connus = set()

    with open(lemmas_file, "r", encoding="utf-8") as f:
        for ligne in f:
            parts = ligne.strip().split("\t")
            if len(parts) == 2:
                mot, lemme = parts
                mot_to_lemme[mot] = lemme
                lemmes_connus.add(lemme)

    return mot_to_lemme, lemmes_connus

def tokeniser(requete):
    return [t.strip().lower() for t in re.findall(r"\w+'|[\w]+", requete, re.UNICODE) if t.strip()]

def lemmatiser(tokens, nlp):
    resultats = []
    for token in tokens:
        lemme = nlp(token)[0].lemma_
        resultats.append((token, lemme))
    return resultats

def est_specifique(terme):
    if re.search(r"\d", terme):
        return True
    else:
        return False

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

def main(requete):
    nlp = spacy.load("fr_core_news_sm")
    mot_to_lemme, lemmes_connus = charger_lexique()

    tokens = tokeniser(requete)
    termes = lemmatiser(tokens, nlp)

    for token, lemme in termes:
        if est_specifique(token):
            print(f"  {token} -> {token} (entité spécifique)")
            continue
        if token in mot_to_lemme:
            print(f"  {token} -> {mot_to_lemme[token]}")
            continue
        candidats = []
        for mot_lexique in mot_to_lemme:
            prox = recherche_prefixe(token, mot_lexique, 3, 4)
            if prox > 60:
                candidats.append(mot_lexique)
        if len(candidats) == 1:
            print(f"  {token} -> {mot_to_lemme[candidats[0]]} (corrigé: {candidats[0]})")
        elif len(candidats) > 1:
            meilleur = min(candidats, key=lambda c: distance_levenshtein(token, c))
            print(f"  {token} -> {mot_to_lemme[meilleur]} (corrigé: {meilleur})")
        else:
            print(f"  {token} -> ??? (aucun candidat trouvé)")


if __name__ == "__main__":
    requete = input("Entrez votre requête : ")
    main(requete)