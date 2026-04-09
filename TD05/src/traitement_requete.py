import re
import calendar

def clean_req(req):
    req_lower = req.lower()
    to_delete = [
        r"je\s+(veux|voudrais)(\s+voir)?\s+les\s+articles\s+(qui\s+parlent|traitant|de\s+la\s+rubrique|liés\s+à\s+la|avec\s+des)?",
    ]
    for pattern in to_delete:
        req_lower = re.sub(pattern, "", req_lower, count=1, flags=re.IGNORECASE).strip()
    return req_lower

def extract_metadonnees(req):
    meta = {}
    rubriques = []
    mois_noms = ["janvier", "février", "mars", "avril",
                 "mai", "juin", "juillet", "août",
                 "septembre", "octobre", "novembre", "décembre"]
    mois_map = {nom: i + 1 for i, nom in enumerate(mois_noms)}

    with open("../../TD03/data/inverse_rubrique.txt", "r", encoding="UTF-8") as file:
        content = file.read()
        for ligne in content.splitlines()[1:]:
            match = re.search(r"\d", ligne)
            rubrique = ligne[:match.start()].strip().lower()
            if rubrique not in rubriques:
                rubriques.append(rubrique)
    rubriques.sort(key=len, reverse=True)

    req_lower = req.lower()

    meta["rubrique"] = None
    for rubrique in rubriques:
        if rubrique in req_lower:
            meta["rubrique"] = rubrique
            req_lower = re.sub(re.escape(rubrique), "", req_lower, count=1, flags=re.IGNORECASE).strip()
            break

    meta["images"] = None
    m = re.search(r"sans\s+images?", req_lower)
    if m:
        meta["images"] = False
        req_lower = req_lower.replace(m.group(0), "").strip()
    elif re.search(r"images?", req_lower):
        meta["images"] = True
        req_lower = re.sub(r"images?", "", req_lower, count=1).strip()

    meta["date_min"] = None
    meta["date_max"] = None

    mois_pattern = "|".join(mois_noms)

    m = re.search(
        rf"entre\s+le\s+(\d{{1,2}})\s+({mois_pattern})\s+(\d{{4}})\s+et\s+le\s+(\d{{1,2}})\s+({mois_pattern})\s+(\d{{4}})",
        req_lower
    )
    if m:
        meta["date_min"] = f"{int(m.group(1)):02d}/{mois_map[m.group(2)]:02d}/{m.group(3)}"
        meta["date_max"] = f"{int(m.group(4)):02d}/{mois_map[m.group(5)]:02d}/{m.group(6)}"
        req_lower = req_lower.replace(m.group(0), "").strip()
    else:
        m = re.search(r"entre\s+(\d{1,2}/\d{2}/\d{4})\s+et\s+(\d{1,2}/\d{2}/\d{4})", req_lower)
        if m:
            meta["date_min"] = m.group(1)
            meta["date_max"] = m.group(2)
            req_lower = req_lower.replace(m.group(0), "").strip()
        else:
            m = re.search(r"entre\s+(\d{4})\s+et\s+(\d{4})", req_lower)
            if m:
                meta["date_min"] = f"01/01/{m.group(1)}"
                meta["date_max"] = f"31/12/{m.group(2)}"
                req_lower = req_lower.replace(m.group(0), "").strip()
            else:
                m = re.search(
                    rf"(?:après|à\s+partir\s+de)\s+(?:le\s+)?(\d{{1,2}})\s+({mois_pattern})\s+(\d{{4}})",
                    req_lower
                )
                if m:
                    meta["date_min"] = f"{int(m.group(1)):02d}/{mois_map[m.group(2)]:02d}/{m.group(3)}"
                    req_lower = req_lower.replace(m.group(0), "").strip()
                else:
                    m = re.search(
                        rf"(?:après|à\s+partir\s+de)\s+({mois_pattern})\s+(\d{{4}})",
                        req_lower
                    )
                    if m:
                        meta["date_min"] = f"01/{mois_map[m.group(1)]:02d}/{m.group(2)}"
                        req_lower = req_lower.replace(m.group(0), "").strip()
                    else:
                        m = re.search(r"(?:après|à\s+partir\s+de)\s+(\d{1,2}/\d{2}/\d{4})", req_lower)
                        if m:
                            meta["date_min"] = m.group(1)
                            req_lower = req_lower.replace(m.group(0), "").strip()
                        else:
                            m = re.search(r"(?:après|à\s+partir\s+de)\s+(\d{4})", req_lower)
                            if m:
                                meta["date_min"] = f"01/01/{m.group(1)}"
                                req_lower = req_lower.replace(m.group(0), "").strip()

                if not meta["date_min"]:
                    m = re.search(
                        rf"(?:du|le)\s+(\d{{1,2}})\s+({mois_pattern})\s+(\d{{4}})",
                        req_lower
                    )
                    if m:
                        date_str = f"{int(m.group(1)):02d}/{mois_map[m.group(2)]:02d}/{m.group(3)}"
                        meta["date_min"] = date_str
                        meta["date_max"] = date_str
                        req_lower = req_lower.replace(m.group(0), "").strip()

                if not meta["date_min"]:
                    m = re.search(
                        rf"(?:au\s+mois\s+de|en)\s+({mois_pattern})\s+(\d{{4}})",
                        req_lower
                    )
                    if m:
                        mois_num = mois_map[m.group(1)]
                        annee = int(m.group(2))
                        dernier_jour = calendar.monthrange(annee, mois_num)[1]
                        meta["date_min"] = f"01/{mois_num:02d}/{m.group(2)}"
                        meta["date_max"] = f"{dernier_jour:02d}/{mois_num:02d}/{m.group(2)}"
                        req_lower = req_lower.replace(m.group(0), "").strip()

                if not meta["date_min"]:
                    m = re.search(r"(?:en|de(?:\s+l'année)?)\s+(\d{4})", req_lower)
                    if m:
                        meta["date_min"] = f"01/01/{m.group(1)}"
                        meta["date_max"] = f"31/12/{m.group(1)}"
                        req_lower = req_lower.replace(m.group(0), "").strip()

    return meta, req_lower


if __name__ == "__main__":
    tests = [
        "Quels sont les articles parus entre le 3 mars 2013 et le 4 mai 2013 évoquant les Etats-Unis ?",
        "Je voudrais les articles de 2011 sur l'enseignement.",
        "quels sont les articles publiés au mois de novembre 2011 portant sur de la recherche.",
        "je voudrais les articles liés à la recherche scientifique publiés en Février 2010.",
        "Chercher les articles dans le domaine industriel et datés à partir de 2012.",
        "J'aimerais la liste des articles écrits après janvier 2014 et qui parlent d'informatique.",
        "Je voudrais les articles qui datent du 1 décembre 2012 et dont la rubrique est Actualités Innovations.",
        "je veux voir les articles de la rubrique Focus et publiés entre 30/08/2011 et 29/09/2011.",
        "Je cherche les articles sur le Changement climatique publiés après 29/09/2011.",
        "Listez-moi les articles qui parlent de 3D et qui sont écrits entre 2010 et 2011.",
        "J'aimerais un article qui parle de biologie et qui date d'après le 2 juillet 2012 ?",
        "Je veux les articles sans image.",
        "Articles contenant une image.",
        "Afficher les articles de la rubrique en direct des laboratoires.",
    ]
    for t in tests:
        #meta, reste = extract_metadonnees(t)
        #print(f"Requête : {t}")
        #print(f"  meta  : {meta}")
        #print(f"  reste : \"{reste}\"")
        #print()
        print(clean_req(t))
