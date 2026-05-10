# LO17 - Indexation et Recherche d'Information

Projet de moteur de recherche sur un corpus d'articles scientifiques issus de l'ADIT.

## Remarque préalable

Les fichiers data ne doivent pas être déplacés.

## Installation

```bash
pip install -r requirements.txt
```

## Lancement du moteur de recherche

```bash
cd TD06/src
streamlit run moteur.py
```

## Structure des données

### `data/` — Corpus et données globales

| Fichier | Description |
|---------|-------------|
| `corpus.xml` | Corpus XML original avec les articles complets (titre, auteur, date, rubrique, texte, images, contact) |
| `corpus_filtered.xml` | Version filtrée du corpus XML |
| `antidictionnaire.txt` | Liste de mots vides (stopwords) : "de", "l'", "et", "à", etc. |
| `substitution.txt` | Table de substitution des tokens (TSV : token → substitution) |
| `tokens.txt` | Liste des tokens avec leurs fréquences |
| `tokentf.txt` | Fréquences TF (Term Frequency) de chaque token |
| `tokenidf.txt` | Scores IDF (Inverse Document Frequency) des tokens |
| `tokentfidf.txt` | Scores TF-IDF combinés |

### `TD01/data/` — Articles HTML bruts

326 fichiers HTML (`67068.htm` à `76516.htm`), chacun correspondant à un article scientifique avec ses métadonnées (titre, auteur, date, bulletin, rubrique, texte).

### `TD03/data/` — Lemmatisation et index inversés

| Fichier | Description |
|---------|-------------|
| `corpus_lematized.xml` | Corpus XML avec titres et textes lemmatisés |
| `lemmas.txt` | Table de correspondance forme → lemme (TSV) |
| `tokens.txt` | Tokens extraits par article (TSV : article_id → token) |
| `tokentf.txt` | Fréquences TF des tokens lemmatisés |
| `tokenidf.txt` | Scores IDF des tokens lemmatisés |
| `racines.txt` | Racines/stems des mots |
| `inverse_titre.txt` | Index inversé sur les titres (TSV : terme → article_id:fréquence) |
| `inverse_texte.txt` | Index inversé sur les textes (TSV : terme → article_id:fréquence) |
| `inverse_auteur.txt` | Index inversé sur les auteurs (TSV : auteur → article_ids) |
| `inverse_bulletin.txt` | Index inversé sur les bulletins (TSV : bulletin → article_ids) |
| `inverse_date.txt` | Index inversé sur les dates (TSV : JJ/MM/AAAA → article_ids) |
| `inverse_rubrique.txt` | Index inversé sur les rubriques (TSV : rubrique → article_ids) |
| `inverse_images.txt` | Index inversé sur les images (TSV : images → article_ids) |

### `TD04/data/` — Correcteur orthographique

| Fichier | Description |
|---------|-------------|
| `lexique.txt` | Lexique de référence pour la correction orthographique (un mot par ligne) |

### `TD06/data/` — Résultats d'évaluation

| Fichier | Description |
|---------|-------------|
| `temps_reponse.png` | Graphique des temps de réponse moyens du moteur sur 100 exécutions par requête |
