import re
import math
import seaborn as sns #type:ignore
import matplotlib.pyplot as plt
from collections import defaultdict

def segmente(xmlfile="../../data/corpus.xml", outputfile="../../data/tokens.txt"):
    with open(xmlfile, 'r', encoding='utf-8') as file:
        content = file.read()
    
    documents = re.findall(r'<document>(.*?)</document>', content, re.DOTALL)

    with open(outputfile, 'w', encoding='utf-8') as out:
        out.write("article\ttoken\n")
        
        for doc in documents:
            article_match = re.search(r'<article>(.*?)</article>', doc)
            num_article = article_match.group(1).strip() if article_match else "unknown"
            
            titre_match = re.search(r'<titre>(.*?)</titre>', doc, re.DOTALL)
            texte_match = re.search(r'<texte>(.*?)</texte>', doc, re.DOTALL)
            
            titre = titre_match.group(1) if titre_match else ""
            texte = texte_match.group(1) if texte_match else ""
            
            contenu_complet = titre + ' ' + texte
            
            tokens = re.findall(r"\d{1,2}/\d{1,2}/\d{4}|\w+'|[\w]+", contenu_complet, re.UNICODE)
            
            for token in tokens:
                token = token.strip().lower()
                if token:
                    out.write(f"{num_article}\t{token}\n")

def calculer_frequences(tokens_file = "../../data/tokens.txt"):
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

    with open("../../data/tokentf.txt", 'w', encoding='utf-8') as out:
        out.write("article\ttoken\tcoef.\n")
        for article in frequences:
            total_tokens = sum(frequences[article].values())
            
            for token, count in frequences[article].items():
                frequence = count / total_tokens
                out.write(f"{article}\t{token}\t{frequence}\n")

def calculer_idf(tokens_file="../../data/tokens.txt"):
    articles = defaultdict(set)
    with open(tokens_file, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            article, token = line.strip().split('\t')
            articles[article].add(token)  # add() ignore les doublons automatiquement
    
    N = len(articles)
    
    d = defaultdict(int)
    for tokens_set in articles.values():
        for token in tokens_set:
            d[token] += 1
    
    with open("../../data/tokenidf.txt", 'w', encoding='utf-8') as out:
        out.write("token\tidf\n")
        for token, df in d.items():
            idf = math.log10(N / df)
            out.write(f"{token}\t{idf:.8f}\n")
        
def calculer_tf_idf(tokenstf_file="../../data/tokentf.txt", tokensidf_file="../../data/tokenidf.txt"):
    from collections import defaultdict
    
    idf_values = {}
    with open(tokensidf_file, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            token, idf = line.strip().split('\t')
            idf_values[token] = float(idf)
    
    token_tfidf_sums = defaultdict(lambda: {'sum': 0, 'count': 0})
    
    with open(tokenstf_file, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            article, token, tf = line.strip().split('\t')
            tf_idf = float(tf) * idf_values.get(token, 0)
            
            token_tfidf_sums[token]['sum'] += tf_idf
            token_tfidf_sums[token]['count'] += 1
    
    token_avg_tfidf = {}
    for token, stats in token_tfidf_sums.items():
        token_avg_tfidf[token] = stats['sum'] / stats['count']
    
    tfidf_data = []
    temp = []
    with open(tokenstf_file, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            article, token, tf = line.strip().split('\t')
            if token not in temp:
                avg_tfidf = token_avg_tfidf[token]
                temp.append(token)
                tfidf_data.append((article, token, avg_tfidf))
    
    tfidf_data.sort(key=lambda x: x[2])
    
    with open("../../data/tokentfidf.txt", 'w', encoding='utf-8') as out:
        out.write("article\ttoken\ttfidf\n")
        for article, token, tf_idf in tfidf_data:
            out.write(f"{article}\t{token}\t{tf_idf:.8f}\n")

def buildAntidictionnaire(tokentfidf_file = "../../data/tokentfidf.txt", seuil=0.0014):
    anti_dictionnaire = []
    with open(tokentfidf_file, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            _, token, idf,  = line.strip().split('\t')
            if float(idf) < seuil:
                if token not in anti_dictionnaire:
                    anti_dictionnaire.append(token)
    return anti_dictionnaire

def buildAntidictionnaireFile(tokentfidf_file = "../../data/tokentfidf.txt", seuil=0.0014):
    anti_dictionnaire = buildAntidictionnaire(tokentfidf_file, seuil)
    removed_token = []
    with open(tokentfidf_file, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            _, token, _ = line.strip().split('\t')
            if token in anti_dictionnaire and token not in  removed_token:
                removed_token.append(token)
    with open("../../data/antidictionnaire.txt", 'w', encoding='utf-8') as out:
        out.write("token\n")
        for token in removed_token:
             out.write(f"{token}\n")

def findSeuil(tokentfidf_file = "../../data/tokentfidf.txt"):
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

def buildSubstitution(tokentfidf_file = "../../data/tokentfidf.txt", seuil=0.0014):
    anti_dictionnaire = buildAntidictionnaire(tokentfidf_file, seuil)
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
    with open("../../data/substitution.txt", 'w', encoding='utf-8') as out:
        out.write("token\tsubstitution\n")
        for token in substitution:
             out.write(f"{token}\t{substitution[token]}\n")

def substitue(text, dictionnaire="../../data/substitution.txt"):
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
    tokens = re.findall(r"\d{1,2}/\d{1,2}/\d{4}|\w+'|[\w]+", text, re.UNICODE)
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
                    cleared_ligne = re.sub(r'<[^>]+>', '', ligne).lower()
                    subsitue_ligne = substitue(cleared_ligne, substitution_file)
                    if ligne.strip().startswith("<titre>"):
                        out.write(f"\t\t<titre>{subsitue_ligne}</titre>\n")
                    else:
                     out.write(f"\t\t<texte>{subsitue_ligne}</texte>\n")
                else:
                    out.write(f"{ligne}\n")



if __name__ == "__main__":
    #segmente()
    calculer_frequences()
    calculer_idf()
    calculer_tf_idf()
    buildAntidictionnaireFile()
    buildSubstitution()
    buildFilteredXML()