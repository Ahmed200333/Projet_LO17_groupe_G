import streamlit as st
import sys
import re
import xml.etree.ElementTree as ET
sys.path.append("../../TD05/src")
from traitement_requete import main as extract_data #type:ignore
import time as t
import matplotlib.pyplot as plt

with open("../../data/corpus.xml", "r", encoding="UTF-8") as f:
    xml_content = f.read()
    xml_content = re.sub(r"&(?!amp;|lt;|gt;|apos;|quot;)", "&amp;", xml_content)
    root = ET.fromstring(xml_content)
    CORPUS = {}
    for doc in root.findall("document"):
        article_id = doc.find("article").text
        CORPUS[article_id] = {
            "titre": doc.find("titre").text or "",
            "date": doc.find("date").text or "",
            "rubrique": doc.find("rubrique").text or "",
            "texte": doc.find("texte").text or "",
        }

REQUETES = ["Quels sont les articles parus entre le 3 mars 2013 et le 4 mai 2013 évoquant les Etats-Unis ?",
            "Je veux les articles de 2014 et de la rubrique Focus et parlant de la santé.",
            "Liste des articles qui parlent soit du CNRS, soit des grandes écoles, mais pas de Centrale Paris.",
            "Je voudrais tout les articles provenant de la rubrique événement et contenant le mot congrès dans le titre.",
            "Je souhaites avoir tout les articles donc la rubrique est focus ou Actualités Innovations et qui contiennent les mots chercheurs et paris.",
            "Lister tous les articles dont la rubrique est Focus et qui ont des images.",
            "Je voudrais tous les bulletins écrits entre 2012 et 2013 mais pas au mois de juin.",
            "je veux voir les articles de la rubrique Focus et publiés entre 30/08/2011 et 29/09/2011.",
            "Je veux les articles qui parlent des systèmes embarqués et non pas la robotique.",
            "Je cherche les articles sur le Changement climatique publiés après 29/09/2011."]

with open("../../TD03/data/inverse_images.txt", "r", encoding="UTF-8") as f:
    ligne_images = f.read().splitlines()[1]
    _, articles_img = ligne_images.split("\t")
    ARTICLES_AVEC_IMAGES = set(articles_img.split(" "))

def date_to_int(date_str):
    j, m, a = date_str.split("/")
    return int(a) * 10000 + int(m) * 100 + int(j)

def date_str_to_mois(date_str):
    mois_noms = ["janvier", "février", "mars", "avril", "mai", "juin",
                 "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    m = int(date_str.split("/")[1])
    return mois_noms[m - 1]

def extract_raw_req_res():
    res = {}
    req1_ids, req2_ids, req3_ids, req4_ids, req5_ids, req6_ids = [],[],[],[],[],[]
    req7_ids, req8_ids, req9_ids, req10_ids = [],[],[],[]
    for article_id, info in CORPUS.items():
        d = date_to_int(info["date"])
        if d >= 20130303 and d <= 20130504 \
        and "etats-unis" in info["texte"].lower():
            req1_ids.append(article_id)
        if d >= 20140101 and d <= 20141231 \
        and "focus" in info["rubrique"].lower() \
        and "santé" in info["texte"].lower():
            req2_ids.append(article_id)
        if  "centrale paris" not in info["texte"].lower()\
        and ("cnrs" in info["texte"].lower() or "grandes écoles" in info["texte"].lower()):
            req3_ids.append(article_id)
        if  "evénement" in info["rubrique"].lower()\
        and "congrès" in info["titre"].lower():
            req4_ids.append(article_id)
        if ("focus" in info["rubrique"].lower() or "actualité" in info["rubrique"].lower()) \
        and "chercheurs" in info["texte"].lower() \
        and "paris" in info["texte"].lower():
            req5_ids.append(article_id)
        if "focus" in info["rubrique"].lower() \
        and article_id in ARTICLES_AVEC_IMAGES:
            req6_ids.append(article_id)
        if d >= 20120101 and d <= 20131231 \
        and date_str_to_mois(info["date"]) != "juin":
            req7_ids.append(article_id)
        if "focus" in info["rubrique"].lower() \
        and d >= 20110830 and d <= 20110929:
            req8_ids.append(article_id)
        if "systèmes embarqués" in info["texte"].lower() \
        and "robotique" not in info["texte"].lower():
            req9_ids.append(article_id)
        if "changement climatique" in info["texte"].lower() \
        and d > 20110929:
            req10_ids.append(article_id)
    res[REQUETES[0]] = req1_ids
    res[REQUETES[1]] = req2_ids
    res[REQUETES[2]] = req3_ids
    res[REQUETES[3]] = req4_ids
    res[REQUETES[4]] = req5_ids
    res[REQUETES[5]] = req6_ids
    res[REQUETES[6]] = req7_ids
    res[REQUETES[7]] = req8_ids
    res[REQUETES[8]] = req9_ids
    res[REQUETES[9]] = req10_ids
    print(req4_ids)
    print(req9_ids)
    return res

def run_moteur(req):
    extracted_data = extract_data(req)
    scores = {}
    resultats_kws = None
    if extracted_data["kws"] != []:
        if extracted_data["champ"] == "titre":
            with open("../../TD03/data/inverse_titre.txt", "r", encoding="UTF-8") as f:
                content = f.read()
        elif extracted_data["champ"] == "contenu":
            with open("../../TD03/data/inverse_texte.txt", "r", encoding="UTF-8") as f:
                content = f.read()
        lignes_index = content.splitlines()[1:]
        for kw in extracted_data["kws"]:
            sous_termes = kw["terme"].split()
            ids_kw = None
            scores_kw = {}
            for sous_terme in sous_termes:
                ids = {}
                for ligne in lignes_index:
                    terme, articles = ligne.split("\t")
                    if sous_terme == terme:
                        for article in articles.split(" "):
                            article_id, freq = article.split(":")
                            ids[article_id] = int(freq)
                        break
                ids_set = set(ids.keys())
                if ids_kw is None:
                    ids_kw = ids_set
                else:
                    ids_kw = ids_kw & ids_set
                for article_id, freq in ids.items():
                    scores_kw[article_id] = scores_kw.get(article_id, 0) + freq
            ids_kw = ids_kw or set()
            if resultats_kws is None:
                resultats_kws = ids_kw
            elif kw["op"] == "AND":
                resultats_kws = resultats_kws & ids_kw
            elif kw["op"] == "OR":
                resultats_kws = resultats_kws | ids_kw
            elif kw["op"] == "NOT":
                resultats_kws = resultats_kws - ids_kw
            for article_id, freq in scores_kw.items():
                if article_id in resultats_kws:
                    scores[article_id] = scores.get(article_id, 0) + freq
    resultats_rub = None
    if extracted_data["rubriques"] != []:
        with open("../../TD03/data/inverse_rubrique.txt", "r", encoding="UTF-8") as f:
            content_rub = f.read()
        
        for rubrique in extracted_data["rubriques"]:
            ids = set()
            for ligne in content_rub.splitlines()[1:]:
                terme, articles = ligne.split("\t")
                if rubrique == terme:
                    ids = set(articles.split(" "))
                    break
            if resultats_rub is None:
                resultats_rub = ids
            elif extracted_data["op_rubriques"] == "OR":
                resultats_rub = resultats_rub | ids
            else:
                resultats_rub = resultats_rub & ids
    resultats_dates = None
    if (extracted_data["date_min"] != None) or (extracted_data["date_max"] != None) or (extracted_data["mois_exclus"] != []):
        with open("../../TD03/data/inverse_date.txt", "r", encoding="UTF-8") as f:
            content_date = f.read()
        resultats_dates = set()
        for ligne in content_date.splitlines()[1:]:
            date_str, articles = ligne.split("\t")
            jour, mois, annee = date_str.split("/")
            date_val = int(annee) * 10000 + int(mois) * 100 + int(jour)
            mois_noms = ["janvier", "février", "mars", "avril", "mai", "juin",
                        "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
            mois_nom = mois_noms[int(mois) - 1]
            if mois_nom in extracted_data["mois_exclus"]:
                continue
            inclure = True
            if extracted_data["date_min"] != None:
                j, m, a = extracted_data["date_min"].split("/")
                date_min_val = int(a) * 10000 + int(m) * 100 + int(j)
                if date_val < date_min_val:
                    inclure = False
            if extracted_data["date_max"] != None:
                j, m, a = extracted_data["date_max"].split("/")
                date_max_val = int(a) * 10000 + int(m) * 100 + int(j)
                if date_val > date_max_val:
                    inclure = False
            if inclure:
                resultats_dates.update(articles.split(" "))
    resultats_images = None
    if extracted_data["images"] != None:
        if extracted_data["images"] == True:
            resultats_images = ARTICLES_AVEC_IMAGES
        else:
            resultats_images = set(CORPUS.keys()) - ARTICLES_AVEC_IMAGES

    resultats_final = None
    for res in [resultats_kws if extracted_data["kws"] != [] else None,
                resultats_rub if extracted_data["rubriques"] != [] else None,
                resultats_dates,
                resultats_images]:
        if res is not None:
            resultats_final = res if resultats_final is None else resultats_final & res

    if resultats_final is not None:
        scores = {k: v for k, v in scores.items() if k in resultats_final}
        for article_id in resultats_final:
            if article_id not in scores:
                scores[article_id] = 0
        resultats_tries = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    else:
        resultats_tries = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return extracted_data, resultats_tries

def app():
    st.title("LO17 - Moteur de recherche")

    requete = st.chat_input("Saisir votre requête: ", key="requete")

    if requete:
        st.write(requete)
        
        extracted_data, resultats_tries = run_moteur(requete)

        tri = st.selectbox("Trier par", ["Pertinence", "Date croissante", "Date décroissante"])
        if tri == "Date croissante":
            resultats_tries = sorted(resultats_tries, key=lambda x: (
                int(CORPUS[x[0]]["date"].split("/")[2]) * 10000 +
                int(CORPUS[x[0]]["date"].split("/")[1]) * 100 +
                int(CORPUS[x[0]]["date"].split("/")[0])
            ) if x[0] in CORPUS else 0)
        elif tri == "Date décroissante":
            resultats_tries = sorted(resultats_tries, key=lambda x: (
                int(CORPUS[x[0]]["date"].split("/")[2]) * 10000 +
                int(CORPUS[x[0]]["date"].split("/")[1]) * 100 +
                int(CORPUS[x[0]]["date"].split("/")[0])
            ) if x[0] in CORPUS else 0, reverse=True)

        st.write(f"**{len(resultats_tries)} résultats trouvés**")

        termes_recherche = [kw["terme"] for kw in extracted_data["kws"]]

        for article_id, score in resultats_tries:
            if article_id not in CORPUS:
                continue
            info = CORPUS[article_id]
            snippet = ""
            texte = info["texte"] if info["texte"] else ""
            mots = texte.split()
            for i, mot in enumerate(mots):
                if any(terme in mot for terme in termes_recherche):
                    debut = max(0, i - 10)
                    fin = min(len(mots), i + 10)
                    snippet = "..." + " ".join(mots[debut:fin]) + "..."
                    break
            if not snippet and mots:
                snippet = " ".join(mots[:20]) + "..."

            with st.expander(f"Article {article_id} — {info['titre']} (score: {score})"):
                st.write(f"**Date :** {info['date']}")
                st.write(f"**Rubrique :** {info['rubrique']}")
                st.write(f"**Extrait :** {snippet}")

def evaluate():
    ground_truth = extract_raw_req_res()
    for requete, expected_ids in ground_truth.items():
        _, resultats_tries = run_moteur(requete)

        expected = set(expected_ids)
        retrieved = set(article_id for article_id, _ in resultats_tries)

        tp = len(expected & retrieved)
        precision = tp / len(retrieved) if retrieved else 0
        rappel = tp / len(expected) if expected else 0

        print(f"Requête: {requete}")
        print(f"  Précision: {precision:.2f}, Rappel: {rappel:.2f}")

def answer_time():
    answer_time = {}
    i = 1
    for req in REQUETES:
        times = []
        for j in range(100):
            print(f"Requêtes [{j}/100][{i}/10]")
            debut = t.time()
            run_moteur(req)
            fin = t.time()
            times.append(fin-debut)
        answer_time[req] = sum(times) / 100
        i += 1
    return answer_time

def get_figure():
    times = answer_time()
    plt.figure(figsize=(12, 5))
    plt.bar(range(1, 11), [times[req] for req in REQUETES])
    plt.xlabel("Requête")
    plt.ylabel("Temps moyen (s)")
    plt.title("Temps de réponse moyen sur 100 exécutions")
    plt.xticks(range(1, 11), [f"R{i}" for i in range(1, 11)])
    plt.tight_layout()
    plt.savefig("../data/temps_reponse.png")
    plt.show()

if __name__ == "__main__":
    # evaluate()
    # app()
    get_figure()