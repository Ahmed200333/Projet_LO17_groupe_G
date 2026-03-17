import re
import math
import seaborn as sns #type:ignore
import matplotlib.pyplot as plt

def segmente(xmlfile, outputfile="tokens.txt"):
    with open(xmlfile, 'r', encoding='utf-8') as file:
        content = file.read()
    
    articles_content = re.findall(r'<article>(.*?)</images>', content, re.DOTALL)
    
    with open(outputfile, 'w', encoding='utf-8') as out:
        out.write("article\ttoken\n")
        
        for c in articles_content:
            titre_match = re.search(r'<titre>(.*?)</titre>', c)
            texte_match = re.search(r'<texte>(.*?)</texte>', c)
            num_article = c[:5]
            
            titre = titre_match.group(1) if titre_match else ""
            texte = texte_match.group(1) if texte_match else ""
            
            contenu_complet = titre + ' ' + texte
            
            tokens = re.findall(r'\b[\w\']+\b', contenu_complet, re.UNICODE)
            
            for token in tokens:
                if token.strip():
                    if "\'" in token:
                        tokens = token.split("\'")
                        out.write(f"{num_article}\t{tokens[0]+'\''}\n")
                        out.write(f"{num_article}\t{tokens[1]}\n")
                    else:
                        out.write(f"{num_article}\t{token}\n")


def calculer_frequences(tokens_file = "tokens.txt"):
    frequences = {}
    
    with open(tokens_file, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            article, token = line.strip().split('\t')
            token = token.lower()
            
            if article not in frequences:
                frequences[article] = {}

            if token in frequences[article]:
                frequences[article][token] += 1
            else:
                frequences[article][token] = 1

    with open("tokentf.txt", 'w', encoding='utf-8') as out:
        out.write("article\ttoken\tcoef.\n")
        for article in frequences:
            total_tokens = sum(frequences[article].values())
            
            for token, count in frequences[article].items():
                frequence = count / total_tokens
                out.write(f"{article}\t{token}\t{frequence}\n")

def calculer_idf(tokenstf_file = "tokentf.txt"):
    d = {}
    articles = []
    with open(tokenstf_file, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            article, token, _ = line.strip().split('\t')
            if token not in d:
                d[token] = 1
            else:
                d[token] += 1
            if article not in articles:
                articles.append(article)
    N = len(articles)
    with open("tokenidf.txt", 'w', encoding='utf-8') as out:
        out.write("token\tidf\n")
        for token in d:
            idf = math.log10(N / d[token])
            out.write(f"{token}\t{idf}\n")
        
def calculer_tf_idf(tokenstf_file = "tokentf.txt", tokensidf_file = "tokenidf.txt"):
    idf_values = {}
    with open(tokensidf_file, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            token, idf = line.strip().split('\t')
            idf_values[token] = float(idf)

    with open(tokenstf_file, 'r', encoding='utf-8') as file:
        next(file)
        with open("tokentfidf.txt", 'w', encoding='utf-8') as out:
            out.write("article\ttoken\ttf*idf\n")
            for line in file:
                article, token, tf = line.strip().split('\t')
                tf_idf = float(tf) * idf_values.get(token, 0)
                out.write(f"{article}\t{token}\t{tf_idf}\n")

def construire_anti_dictionnaire(tokentfidf_file = "tokentfidf.txt", seuil=0.1):
    anti_dictionnaire = []
    with open(tokentfidf_file, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            _, token, idf,  = line.strip().split('\t')
            if float(idf) < seuil:
                if token not in anti_dictionnaire:
                    anti_dictionnaire.append(token)
    return anti_dictionnaire


def findSeuil(tokentfidf_file = "tokentfidf.txt"):
    idf_values = []
    with open(tokentfidf_file, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            _, _, idf = line.strip().split('\t')
            idf_values.append(float(idf))
    idf_values.sort()
    filtered = [x for x in idf_values if x > 0.006]
    sns.histplot(filtered, bins=50, kde=True)
    plt.show()


def buildSubstitution(tokentfidf_file = "tokentfidf.txt", seuil=0.09):
    anti_dictionnaire = construire_anti_dictionnaire(tokentfidf_file, seuil)
    substitution = {}
    alltokens = []
    with open(tokentfidf_file, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            _, token, _ = line.strip().split('\t')
            alltokens.append(token)
    for token in alltokens:
        if token in anti_dictionnaire:
            substitution[token] = ""
        else:
            substitution[token] = token
    with open("substitution.txt", 'w', encoding='utf-8') as out:
        out.write("token\tsubstitution\n")
        for token in substitution:
             out.write(f"{token}\t{substitution[token]}\n")


def substitue(text, dictionnaire="substitution.txt"):
    substitution = {}
    with open(dictionnaire, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            if len(line.strip().split('\t')) == 2:
                token, sub = line.strip().split('\t')
            else: 
                token = line.strip()
                sub = ""
            substitution[token] = sub
    tokens = re.findall(r'\b[\w\']+\b', text, re.UNICODE)
    result = []
    for token in tokens:
        mapped = substitution.get(token, token)
        if mapped:
            result.append(mapped)
    return ' '.join(result)

def buildFilteredXML(input_xml="../../data/corpus.xml", output_xml="../../data/corpus_filtered.xml", substitution_file="../../data/substitution.txt"):
    with open(input_xml, 'r', encoding='utf-8') as file:
        content = file.read()
    
        with open(output_xml, 'w', encoding='utf-8') as out:
            for ligne in content.splitlines():
                if ligne.strip().startswith("<titre>") or ligne.strip().startswith("<texte>"):
                    cleared_ligne = re.sub(r'<[^>]+>', '', ligne)
                    subsitue_ligne = substitue(cleared_ligne, substitution_file)
                    if ligne.strip().startswith("<titre>"):
                        out.write(f"\t\t<titre>{subsitue_ligne}</titre>\n")
                    else:
                     out.write(f"\t\t<texte>{subsitue_ligne}</texte>\n")
                else:
                    out.write(f"{ligne}\n")


if __name__ == "__main__":
    buildFilteredXML()


