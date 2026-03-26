import spacy #type: ignore
import re
from nltk.stem import SnowballStemmer
from collections import defaultdict

def applySpacy(text, nlp):
    doc = nlp(text)
    return [(token.text, token.lemma_) for token in doc]

def buildLemmasFromSpacy():
    nlp = spacy.load("fr_core_news_sm")
    mot_lemme = {}

    with open("../../data/corpus_filtered.xml", 'r', encoding='utf-8') as file:
        content = file.read()

    for ligne in content.splitlines():
        if ligne.strip().startswith("<titre>") or ligne.strip().startswith("<texte>"):
            cleared_ligne = re.sub(r'<[^>]+>', '', ligne).strip()
            for mot in cleared_ligne.split():
                if mot not in mot_lemme:
                    lemme = nlp(mot)[0].lemma_
                    mot_lemme[mot] = lemme


    with open("../../data/lemmas.txt", 'w', encoding='utf-8') as out:
        for mot, lemme in sorted(mot_lemme.items()):
            out.write(f"{mot}\t{lemme}\n")

def buildRacineFromNLTK():
    stemmer = SnowballStemmer("french")
    mot_racine = {}
    with open("../../data/corpus_filtered.xml", 'r', encoding='utf-8') as file:
        content = file.read()
    for ligne in content.splitlines():
        if ligne.strip().startswith("<titre>") or ligne.strip().startswith("<texte>"):
            cleared_ligne = re.sub(r'<[^>]+>', '', ligne).strip()
            for mot in cleared_ligne.split():
                if mot not in mot_racine:
                    racine = stemmer.stem(mot)
                    mot_racine[mot] = racine

    with open("../../data/racines.txt", 'w', encoding='utf-8') as out:
        for mot, racine in sorted(mot_racine.items()):
            out.write(f"{mot}\t{racine}\n")

def getUniqueLemmeAndRacine():
    lemmas = open("../../data/lemmas.txt", "r", encoding='utf-8')
    unique_lemme = []
    content_lemmas = lemmas.read()
    for ligne in content_lemmas.splitlines():
        _, lemme = ligne.split("\t")
        if lemme not in unique_lemme:
            unique_lemme.append(lemme)
    racines = open("../../data/racines.txt", "r", encoding='utf-8')
    unique_racine = []
    content_racines = racines.read()
    for ligne in content_racines.splitlines():
        _, racine = ligne.split("\t")
        if racine not in unique_racine:
            unique_racine.append(racine)
    print(len(unique_lemme),len(unique_racine))

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


if __name__ == "__main__":
    buildLemmasFromSpacy()
    # buildRacineFromNLTK()
    # getUniqueLemmeAndRacine()