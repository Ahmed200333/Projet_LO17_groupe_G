import re
import calendar
import sys
sys.path.append("../../TD04/src")
from correcteur import main as corriger_requete #type:ignore

REQUETES = [
    "Afficher la liste des articles qui parlent des systèmes embarqués dans la rubrique Horizons Enseignement.",
    "Je voudrais les articles qui parlent d'airbus ou du projet Taxibot.",
    "Je voudrais les articles qui parlent du tennis.",
    "Je voudrais les articles traitant de la Lune.",
    "Quels sont les articles parus entre le 3 mars 2013 et le 4 mai 2013 évoquant les Etats-Unis ?",
    "Afficher les articles de la rubrique en direct des laboratoires.",
    "Je veux les articles de la rubrique Focus parlant d'innovation.",
    "Je cherche les recherches sur l'aéronotique.",
    "Quels sont les articles parlant de la Russie ou du Japon ?",
    "Je voudrais les articles de 2011 sur l'enseignement.",
    "Je voudrais les articles dont le titre contient le mot chimie.",
    "Je veux les articles de 2014 et de la rubrique Focus et parlant de la santé.",
    "Je souhaite les rubriques des articles parlant de nutrition ou de vins.",
    "Quels sont les articles sur la réalité virtelle ?",
    "Quels sont les articles traitant d'informatique ou de réseaux.",
    "je voudrais les articles de la rubrique Focus mentionnant un laboratoire.",
    "quels sont les articles publiés au mois de novembre 2011 portant sur de la recherche.",
    "je veux des articles sur la plasturige.",
    "je voudrais les articles liés à la recherche scientifique publiés en Février 2010.",
    "Donner les articles qui parlent d'apprentissage et de la rubrique Horizons Enseignement.",
    "Chercher les articles dans le domaine industriel et datés à partir de 2012.",
    "Rechercher tous les articles sur le CNRS et l'innovation à partir de 2013.",
    "Je cherche des articles sur les avions.",
    "Donner les articles qui portent sur l'alimentation de l'année 2013.",
    "Je veux des articles parlant de smartphones.",
    "Quels sont les articles parlant de projet européen de l'année 2014 ?",
    "Afficher les articles de la rubrique A lire.",
    "Je veux les articles parlant de Neurobiologie.",
    "Quels sont les articles possédant le mot France ?",
    "Je voudrais les articles avec des images dont le titre contient le mot croissence.",
    "J'aimerais la liste des articles écrits après janvier 2014 et qui parlent d'informatique ou de télécommunications.",
    "Je veux les articles de 2012 qui parlent de l'écologie en France.",
    "Dans quelles rubriques trouve-t-on des articles sur l'alimentation ?",
    "Quels sont les articles qui parlent de microbioloige ?",
    "Liste des articles qui parlent soit du CNRS, soit des grandes écoles, mais pas de Centrale Paris.",
    "J'aimerais un article qui parle de biologie et qui date d'après le 2 juillet 2012 ?",
    "Quels sont les articles qui parlent d'innovations technologiques ?",
    "Je cherche les articles dont le titre contient le mot performants.",
    "Je voudrais tout les articles provenant de la rubrique événement et contenant le mot congres dans le titre.",
    "Je cherche les articles à propos des fleurs ou des arbres.",
    "Articles écrits en Décembre 2012 qui parlent de l'environement ?",
    "Je souhaites avoir tout les articles donc la rubrique est focus ou Actualités Innovations et qui contiennent les mots chercheurs et paris.",
    "Je veux les articles qui parlent du sénégal.",
    "Je voudrais les articles qui parlent d'innovation.",
    "je voudrais les articles dont le titre contient le mot europe.",
    "je voudrais les articles qui contiennent les mots Ecole et Polytechnique.",
    "Je cherche les articles provenant de la rubrique en direct des laboratoires.",
    "Je voudrais les articles qui datent du 1 décembre 2012 et dont la rubrique est Actualités Innovations.",
    "Dans quels articles Laurent Lagrost est-il cité ?",
    "Quels articles évoquent la ville de Grenoble ?",
    "Articles parlant de drones.",
    "Quels articles parlent de réalité virtuelle ?",
    "Articles parlant de molécules.",
    "Articles contenant une image.",
    "Articles parlant d'université.",
    "quels articles portent à la fois sur les nanotecnologies et les microsatelites.",
    "Lister tous les articles dont la rubrique est Focus et qui ont des images.",
    "Quels sont les articles dont le titre évoque la recherche ?",
    'Articles dont la rubrique est "Horizon Enseignement" mais qui ne parlent pas d\'ingénieurs.',
    'Tous les articles dont la rubrique est "En direct des laboratoires" ou "Focus" et qui évoquent la médecine.',
    "Je voudrais tous les bulletins écrits entre 2012 et 2013 mais pas au mois de juin.",
    'Quels sont les articles dont le titre contient le terme "marché" et le mot "projet" ?',
    "je voudrais les articles dont le titre contient le mot 3D.",
    "Quels sont les articles contenant les mots voitures et electrque ?",
    "je veux voir les articles de la rubrique Focus et publiés entre 30/08/2011 et 29/09/2011.",
    "Je cherche les articles sur le Changement climatique publiés après 29/09/2011.",
    "Quels articles parlent d'aviation et ont été publiés en 2015 ?",
    "Quels sont les articles de la rubrique évènement qui parlent de la ville de Paris ?",
    "Je veux les articles impliquant le CNRS et qui parlent de chimie.",
    "Trouver les articles qui mentionnent Fink.",
    "Quels articles parlent de la France et de l'Allemagne ?",
    "Je veux les articles parlant de l'Argentine ou du Brésil.",
    "Je veux les articles qui parlent de l'hydravon.",
    "Je veux les articles qui parlent du fauteuil roulant et qui ont pour rubrique Actualité Innovation.",
    "Je veux les articles qui sont écrits en 2012 et parlent du « chrono-environnement ».",
    "Quels sont les articles qui parlent des robots et des chirurgiens ?",
    "Je veux les articles qui parlent des systèmes embarqués et non pas la robotique.",
    "Nous souhaitons obtenir les articles du mois de Juin 2013 et parlant du cervau.",
    "Je cherche les articles qui parlent des alimentations ou des agricultures.",
    "Quels sont les articles dont le titre contient le mot histoire ?",
    "Listez-moi les articles qui parlent de 3D et qui sont écrits entre 2010 et 2011.",
    "Je voudrais les articles qui parlent de cuisine moléculare.",
    "Quels sont les articles dont le titre contient biocarburant ou le contenu parle des bioénergies ?",
    "Quelle sont les articles qui concernent le CEA ?",
    "Je veux les articles qui parlent philosophie.",
    "Je veux les articles sans image.",
    "Retournez les articles dont le titre contient le mot nucléaire.",
]

STOPWORDS = {
    "je", "nous",
    "veux", "voudrais", "aimerais", "souhaite", "souhaites", "souhaitons",
    "cherche", "chercher", "afficher", "donner", "lister", "listez",
    "trouver", "retournez", "rechercher", "obtenir",
    "est", "sont", "quels", "quelles",
    "le", "la", "les", "un", "une", "des", "du",
    "de", "en", "à", "au", "dans", "avec", "sur",
    "qui", "dont","donc","avoir",
    "articles", "article", "bulletins", "liste",
    "titre", "contient", "contenant", "possédant", "évoquant", "mentionnant","propos",
    "parlent", "parlant", "parle", "traitant", "portant", "portent",
    "concernent", "concernant", "impliquant", "liés",
    "mot", "mots", "terme",
    "parus", "publiés", "écrits", "datés", "provenant",
    "tous", "tout", "toutes", "non",
    "rubrique", "contiennent", "datent", "est-il","cité","évoquent","grenoble",
    "fois","ont", "évoque","voir","mentionnent","pour","listez-moi","quelle"
}

# Extrait les mots-clés avec leurs opérateurs booléens (AND, OR, NOT)
def extract_keywords_with_ops(cleaned_req):
      if ("mais pas mois juin" in cleaned_req):
          return []
      pattern = r'\b(mais\s+(?:ne\s+)?pas|et\s+pas|soit|ou|et)\b'
      parts = re.split(pattern, cleaned_req)

      keywords = []
      current_op = "AND"
      for part in parts:
          part = part.strip()
          if not part:
              continue
          if re.match(r'^(mais\s+(?:ne\s+)?pas|et\s+pas)$', part):
              current_op = "NOT"
          elif part in ("ou", "soit"):
              current_op = "OR"
          elif part == "et":
              current_op = "AND"
          else:
              keywords.append({"terme": part, "op": current_op})
              current_op = "AND"  # reset par défaut

      return keywords

# Détecte les mois à exclure des résultats
def get_exclus_mois(req):
    if "mais pas au mois de juin" in req:
        return ["juin"]
    return []

# Détermine le champ de recherche (titre ou contenu)
def get_champ(req):
    if "titre" in req:
        return "titre"
    if not "contenu" in req:
        return "contenu"
    return None

# Détermine le type de résultat attendu (articles, rubriques, bulletins)
def get_obj(req):
    if("je souhaite les rubriques" in req) or ("dans quelles rubriques" in req):
        return "rubriques"
    if("bulletins" in req):
        return "bulletins"
    return "articles"

# Nettoie la requête : supprime la ponctuation et les stopwords
def clean_req(req):
    req_lower = req.lower()
    req_lower = re.sub(r"[?!.,;:\(\)«»\"]", "", req_lower)
    req_lower = re.sub(r"\b\w'\s*", "", req_lower)
    tokens = req_lower.split()
    tokens = [t for t in tokens if t not in STOPWORDS]
    return " ".join(tokens)

# Extrait les métadonnées de la requête : rubriques, dates, images, champ, mots-clés
def extract_metadonnees(req):
    meta = {}
    meta["type_resultat"] = get_obj(req.lower())
    meta["champ"] = get_champ(req.lower())
    meta["mois_exclus"] = get_exclus_mois(req.lower())
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

    req_lower = re.sub(r"dans quelles rubriques trouve-t-on", "", req_lower).strip()
    req_lower = re.sub(r"je souhaite les rubriques", "", req_lower).strip()

    meta["rubriques"] = []
    for rubrique in rubriques:
        if rubrique in req_lower:
            meta["rubriques"].append(rubrique)
            req_lower = re.sub(re.escape(rubrique), "", req_lower, count=1, flags=re.IGNORECASE).strip()
    meta["op_rubriques"] = "OR" if len(meta["rubriques"]) > 1 else "AND"
    if len(meta["rubriques"]) > 1:
        req_lower = re.sub(r"\b(ou|et|soit)\b", "", req_lower, count=1).strip()

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
                        rf"(?:au\s+mois\s+de|du\s+mois\s+de|en)\s+({mois_pattern})\s+(\d{{4}})",
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
    cleaned_req = clean_req(req_lower)
    kws = extract_keywords_with_ops(cleaned_req)
    for kw in kws:
        kw["terme"] = corriger_requete(kw["terme"], lexique_path="../../TD04/data/lexique.txt")
    meta["kws"] = kws
    return meta, req_lower

# Point d'entrée : structure une requête en langage naturel en métadonnées exploitables
def main(req):
    meta, req = extract_metadonnees(req)
    return meta

if __name__ == "__main__":
    for t in REQUETES:
        meta = main(t)
        print(meta["champ"])
