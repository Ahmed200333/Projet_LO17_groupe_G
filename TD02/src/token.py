import re
import math

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

def construire_anti_dictionnaire(tokentfidf_file = "tokentfidf.txt", seuil=0.008):
    anti_dictionnaire = []
    with open(tokentfidf_file, 'r', encoding='utf-8') as file:
        next(file)
        for line in file:
            _, token, idf,  = line.strip().split('\t')
            if float(idf) < seuil:
                if token not in anti_dictionnaire:
                    anti_dictionnaire.append(token)
    return anti_dictionnaire

# segmente("../../TD01/src/output.xml")

# calculer_frequences("tokens.txt")

# calculer_idf()

# calculer_tf_idf()

print(construire_anti_dictionnaire())
