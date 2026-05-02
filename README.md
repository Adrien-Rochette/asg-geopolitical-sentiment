# ASG - Analyseur de Sentiments Géopolitiques

J’ai construit une application Full-Stack AI capable d’analyser des titres géopolitiques. Le système collecte des titres, les envoie à un backend TypeScript, appelle un microservice Python contenant un modèle PyTorch, sauvegarde les résultats dans PostgreSQL, puis affiche des statistiques par région dans un dashboard. Le projet est entièrement conteneurisé avec Docker Compose.

## 1. Qu’est-ce que ce projet et à quoi sert-il ?

ASG, pour **Analyseur de Sentiments Géopolitiques**, est une application Full-Stack AI qui analyse automatiquement des titres d’actualité internationale afin d’en déduire une tonalité générale :

- positive ;
- neutre ;
- négative.

L’objectif du projet est de construire une chaîne complète allant de la collecte de titres jusqu’à leur visualisation dans un tableau de bord.

Ce projet a été conçu comme un projet de démonstration technique pour un entretien d’embauche. Il montre la capacité à construire une application complète autour d’un modèle de machine learning, en combinant :

- un modèle PyTorch entraîné sur du texte ;
- une API Python FastAPI pour exposer le modèle ;
- un backend NodeJS / TypeScript pour orchestrer les traitements ;
- une base PostgreSQL pour stocker les prédictions ;
- Docker Compose pour lancer toute l’architecture ;
- un dashboard minimal pour visualiser les résultats.

L’intérêt du projet n’est pas seulement de prédire un sentiment. Il est surtout de démontrer une compréhension concrète d’un pipeline machine learning complet :

```text
données textuelles
→ prétraitement
→ transformation en tenseurs
→ modèle PyTorch
→ prédiction
→ API
→ stockage
→ statistiques
→ dashboard


## 2. Quelles sont les fonctionnalités du projet ?

Le projet permet actuellement de :

Côté machine learning : 
- transformer un titre en tokens ;
- construire un vocabulaire mot → identifiant numérique ;
- gérer les mots inconnus avec un token <UNK> ;
- gérer le padding avec un token <PAD> ;
- convertir les titres en tenseurs PyTorch ;
- utiliser une couche d’embedding ;
- entraîner un classifieur de texte PyTorch ;
- sauvegarder le modèle entraîné ;
- recharger le modèle pour faire des prédictions ;
- retourner un sentiment parmi :
    - positive
    - neutral
    - negative.
Côté API Python : 
- exposer une route de santé :
- GET /health
- xposer une route de prédiction :
- POST /predict

Exemple de requête :

{
  "text": "Peace agreement brings hope"
}

Exemple de réponse :

{
  "text": "Peace agreement brings hope",
  "sentiment": "positive",
  "confidence": 0.99
}

Côté backend TypeScript
exposer une route de santé :
GET /health
recevoir un titre à analyser :
POST /analyze
appeler automatiquement le microservice Python ;
sauvegarder le résultat en base PostgreSQL ;
récupérer les derniers titres analysés :
GET /headlines
calculer des statistiques par région :
GET /stats
fournir les données du dashboard :
GET /dashboard-data
servir une page dashboard :
GET /dashboard
Côté base de données
stocker les titres analysés ;
stocker le sentiment prédit ;
stocker la confiance du modèle ;
stocker la source ;
stocker la région ;
stocker la date d’insertion.
Côté dashboard

Le dashboard affiche :

les statistiques par région ;
le nombre de titres positifs ;
le nombre de titres neutres ;
le nombre de titres négatifs ;
un score moyen de moral par région ;
la confiance moyenne du modèle ;
les derniers titres analysés.
Côté Docker

Le projet peut être lancé avec une seule commande :

docker compose up --build

Cette commande lance :

PostgreSQL ;
le microservice Python FastAPI ;
le backend TypeScript ;
le dashboard servi par le backend.


## 3. Comment le projet fonctionne-t-il techniquement ?

Architecture générale : 

Collecteur manuel
      ↓
Backend TypeScript
      ↓
Microservice Python FastAPI
      ↓
Modèle PyTorch
      ↓
PostgreSQL
      ↓
Dashboard

Détail du flux
1. Le collecteur envoie un titre au backend TypeScript.
2. Le backend reçoit le titre via la route POST /analyze.
3. Le backend appelle le microservice Python via la route POST /predict.
4. Le microservice Python encode le texte.
5. Le modèle PyTorch produit des logits.
6. Les logits sont transformés en probabilités avec softmax.
7. La classe ayant la probabilité la plus élevée est sélectionnée.
8. Le backend sauvegarde le titre, le sentiment, la confiance, la région et la source dans PostgreSQL.
9. Le dashboard interroge le backend pour afficher les statistiques.

# Stack technique

- Intelligence artificielle : 
Python
PyTorch
FastAPI
Uvicorn

- Backend :
NodeJS
TypeScript
Express
Axios
pg

- Base de données : 
PostgreSQL

- Conteneurisation :

Docker
Docker Compose

- Dashboard :
HTML
CSS
JavaScript natif

# Structure du projet :
asg-geopolitical-sentiment/
│
├── ai-service/
│   ├── app.py
│   ├── model.py
│   ├── train.py
│   ├── predict.py
│   ├── data.csv
│   ├── requirements.txt
│   └── Dockerfile
│
├── backend/
│   ├── src/
│   │   ├── server.ts
│   │   ├── db.ts
│   │   └── services/
│   │       └── sentiment.service.ts
│   ├── public/
│   │   └── dashboard.html
│   ├── package.json
│   └── Dockerfile
│
├── database/
│   └── init.sql
│
├── scraper/
│   └── manual_collector.py
│
├── experiments/
│   └── fichiers de démonstration PyTorch
│
├── docker-compose.yml
└── README.md


# Lancement du projet
1. Lancer tous les services

À la racine du projet :

docker compose up --build
2. Tester le backend
http://127.0.0.1:3000/health
3. Tester le service IA
http://127.0.0.1:8000/health
4. Accéder au dashboard
http://127.0.0.1:3000/dashboard
5. Envoyer un titre à analyser
Invoke-RestMethod `
  -Uri "http://127.0.0.1:3000/analyze" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"text": "Peace agreement brings hope", "source": "manual", "region": "Europe"}'



## 4. Quelles sont les choses techniques à retenir sur le machine learning ?
1. Un modèle ne comprend pas directement le texte

Un titre comme :

Peace talks resume between two countries

doit être transformé en données numériques.

Le pipeline utilisé est :

texte brut
→ tokens
→ identifiants numériques
→ tenseur PyTorch
→ embeddings
→ classifieur
2. La tokenisation est la première étape du traitement du langage

La tokenisation permet de passer de :

Peace talks resume

à :

["peace", "talks", "resume"]

Cette étape montre une idée fondamentale du NLP : il faut découper le texte pour le rendre exploitable.

3. Le vocabulaire permet de transformer les mots en identifiants

Le modèle ne manipule pas directement les mots. Il manipule des identifiants numériques.

Exemple :

{
  "<PAD>": 0,
  "<UNK>": 1,
  "peace": 2,
  "talks": 3
}

Un titre peut alors devenir :

[2, 3, 4, 0, 0, 0]
4. <PAD> et <UNK> ont deux rôles différents

<PAD> sert à compléter les phrases pour qu’elles aient toutes la même longueur.

<UNK> sert à représenter un mot inconnu du vocabulaire.

<UNK> = mot présent mais inconnu
<PAD> = absence de mot, remplissage artificiel
5. Le padding est nécessaire pour entraîner par batch

PyTorch traite plusieurs exemples en même temps.

Pour créer un batch, toutes les entrées doivent avoir la même longueur.

Exemple :

[2, 3, 4]

devient :

[2, 3, 4, 0, 0, 0, 0, 0]
6. Les embeddings transforment les mots en vecteurs

Une couche Embedding transforme un identifiant de mot en vecteur dense.

Exemple conceptuel :

peace → 2 → [0.12, -0.45, 0.33, ...]

Cela permet au modèle d’apprendre une représentation numérique des mots.

7. Le modèle produit des logits, pas directement des probabilités

Le modèle retourne des scores bruts appelés logits.

Ces logits sont ensuite transformés en probabilités avec :

torch.softmax(logits, dim=1)

La classe prédite est obtenue avec :

torch.argmax(probabilities, dim=1)
8. La loss mesure l’erreur du modèle

Le projet utilise :

nn.CrossEntropyLoss()

Cette fonction est adaptée à la classification multi-classes.

Elle compare :

prédiction du modèle
vs
label réel
9. La backpropagation ajuste les poids

La séquence d’entraînement PyTorch utilisée est :

optimizer.zero_grad()
logits = model(input_ids)
loss = criterion(logits, y_true)
loss.backward()
optimizer.step()

Elle signifie :

effacer les anciens gradients
faire une prédiction
calculer l’erreur
calculer les gradients
mettre à jour les poids
10. Le modèle actuel est volontairement simple

Le modèle utilise :

Embedding
→ moyenne des embeddings
→ couche linéaire
→ ReLU
→ couche linéaire
→ logits

Ce choix est pédagogique. Il permet de comprendre les bases de PyTorch sans dépendre directement d’un modèle pré-entraîné comme BERT.

Limites connues

Le projet fonctionne techniquement, mais il a plusieurs limites importantes :

le dataset est très petit ;
le modèle peut surapprendre les exemples ;
la confiance affichée peut être trop élevée ;
le sentiment géopolitique est subjectif ;
le modèle ne comprend pas réellement le contexte politique ;
les régions sont fournies manuellement ;
le scraper est manuel et non connecté à une vraie source d’actualité.

Ces limites sont importantes à mentionner en entretien. Elles montrent que le projet est compris de manière critique.

Améliorations futures

Améliorations possibles :

utiliser un vrai dataset de sentiment analysis ;
collecter des titres depuis des flux RSS publics ;
ajouter une étape de validation du modèle ;
ajouter des métriques comme l’accuracy ou la matrice de confusion ;
utiliser un modèle plus avancé comme LSTM, GRU ou Transformer ;
comparer le modèle custom avec un modèle pré-entraîné ;
ajouter un vrai frontend React ;
ajouter des graphiques dans le dashboard ;
ajouter des tests unitaires ;
ajouter une pipeline CI/CD ;
déployer le projet sur un cloud provider.
Statut

Le projet est actuellement un MVP fonctionnel et présentable.


---

## `ai-service/README.md`

```markdown
# AI Service

Ce dossier contient le microservice d’intelligence artificielle du projet ASG.

Il regroupe :

- le modèle PyTorch ;
- le script d’entraînement ;
- le script de prédiction ;
- l’API FastAPI ;
- les données d’entraînement ;
- le Dockerfile du service IA.

## Rôle dans l’architecture

Le service IA reçoit un titre d’actualité et retourne :

- le texte analysé ;
- le sentiment prédit ;
- la confiance du modèle.

Il est appelé par le backend TypeScript.

```text
Backend TypeScript
      ↓
AI Service FastAPI
      ↓
Modèle PyTorch
Fichiers principaux
ai-service/
├── app.py
├── model.py
├── train.py
├── predict.py
├── data.csv
├── requirements.txt
└── Dockerfile
model.py

Contient la classe SentimentClassifier.

Architecture du modèle :

Embedding
→ moyenne des embeddings
→ Linear
→ ReLU
→ Linear
→ logits

Le modèle prend en entrée un tenseur d’identifiants de mots :

[batch_size, sequence_length]

et retourne des logits :

[batch_size, num_classes]

Les trois classes sont :

negative
neutral
positive
train.py

Script d’entraînement du modèle.

Il réalise les étapes suivantes :

lecture de data.csv ;
construction du vocabulaire ;
encodage des textes ;
transformation en tenseurs PyTorch ;
entraînement du modèle ;
sauvegarde dans sentiment_model.pt.

Commande :

python train.py
predict.py

Script de prédiction.

Il recharge :

les poids du modèle ;
le vocabulaire ;
la longueur maximale utilisée pendant l’entraînement.

Puis il prédit le sentiment d’un nouveau titre.

Commande :

python predict.py
app.py

Expose le modèle avec FastAPI.

Routes disponibles :

GET /health
POST /predict

Exemple de requête :

{
  "text": "Peace agreement brings hope"
}

Exemple de réponse :

{
  "text": "Peace agreement brings hope",
  "sentiment": "positive",
  "confidence": 0.99
}
Lancement local

Créer et activer l’environnement Python :

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Installer les dépendances :

pip install -r requirements.txt

Entraîner le modèle :

python train.py

Lancer l’API :

uvicorn app:app --reload --port 8000

Tester :

http://127.0.0.1:8000/health

Documentation automatique FastAPI :

http://127.0.0.1:8000/docs
Lancement avec Docker

Depuis la racine du projet :

docker compose up --build

Le service IA sera disponible sur :

http://127.0.0.1:8000
Remarque sur sentiment_model.pt

Le fichier sentiment_model.pt contient le modèle entraîné.

Il est ignoré par Git pour éviter de versionner des fichiers binaires potentiellement lourds.

Pour le recréer :

python train.py
Limites

Le dataset utilisé est volontairement petit.

Le modèle est pédagogique et ne doit pas être interprété comme un système fiable de compréhension géopolitique.

Son objectif est de montrer :

la construction d’un pipeline NLP ;
la manipulation de tenseurs ;
l’utilisation d’embeddings ;
l’entraînement PyTorch ;
l’exposition d’un modèle via API.

---

## `backend/README.md`

```markdown
# Backend TypeScript

Ce dossier contient le backend NodeJS / TypeScript du projet ASG.

Il joue le rôle d’orchestrateur entre :

- le client ;
- le microservice Python ;
- la base PostgreSQL ;
- le dashboard.

## Rôle dans l’architecture

Le backend reçoit les titres à analyser, appelle le service IA, sauvegarde les résultats en base, puis expose des routes de consultation.

```text
Client
  ↓
Backend TypeScript
  ↓
AI Service Python
  ↓
PostgreSQL
Technologies utilisées
NodeJS
TypeScript
Express
Axios
pg
Docker
Fichiers principaux
backend/
├── src/
│   ├── server.ts
│   ├── db.ts
│   └── services/
│       └── sentiment.service.ts
├── public/
│   └── dashboard.html
├── package.json
├── tsconfig.json
└── Dockerfile
Routes disponibles
Santé du backend
GET /health

Réponse :

{
  "status": "ok",
  "service": "asg-backend"
}
Analyser un titre
POST /analyze

Exemple :

{
  "text": "Peace agreement brings hope",
  "source": "manual",
  "region": "Europe"
}

Cette route :

reçoit le titre ;
appelle le microservice Python ;
récupère le sentiment prédit ;
sauvegarde le résultat dans PostgreSQL ;
retourne la ligne sauvegardée.
Récupérer les titres analysés
GET /headlines

Retourne les derniers titres sauvegardés en base.

Récupérer les statistiques
GET /stats

Retourne les statistiques par région :

nombre total de titres ;
nombre de titres positifs ;
nombre de titres neutres ;
nombre de titres négatifs ;
score moyen de moral ;
confiance moyenne.
Données du dashboard
GET /dashboard-data

Retourne :

les statistiques par région ;
les derniers titres analysés.
Dashboard
GET /dashboard

Affiche une page HTML simple avec les statistiques du projet.

Lancement local

Installer les dépendances :

npm install

Lancer en développement :

npm run dev

Compiler :

npm run build

Lancer la version compilée :

npm start
Variables d’environnement

Le backend utilise les variables suivantes :

PORT
AI_SERVICE_URL
DB_HOST
DB_PORT
DB_USER
DB_PASSWORD
DB_NAME

En local, des valeurs par défaut sont utilisées.

Dans Docker Compose, elles sont définies dans docker-compose.yml.

Lancement avec Docker

Depuis la racine du projet :

docker compose up --build

Le backend sera disponible sur :

http://127.0.0.1:3000
Dashboard

Une fois les services lancés, accéder à :

http://127.0.0.1:3000/dashboard
Rôle technique

Ce backend montre :

la création d’une API REST ;
la communication entre services ;
l’appel HTTP vers un modèle IA ;
l’utilisation d’une base PostgreSQL ;
la séparation entre logique backend et logique IA ;
la préparation de données pour un dashboard.

---

## `scraper/README.md`

```markdown
# Scraper / Collecteur

Ce dossier contient le collecteur de titres du projet ASG.

Pour le moment, il s’agit d’un collecteur manuel contrôlé, et non d’un scraper web réel.

## Rôle

Le collecteur envoie une liste de titres au backend TypeScript.

Le backend se charge ensuite :

1. d’appeler le modèle IA ;
2. de récupérer le sentiment ;
3. de sauvegarder le résultat dans PostgreSQL.

```text
manual_collector.py
      ↓
POST /analyze
      ↓
Backend TypeScript
      ↓
AI Service Python
      ↓
PostgreSQL
Fichier principal
scraper/
└── manual_collector.py
Fonctionnement

Le fichier contient une liste de titres sous cette forme :

{
    "text": "Peace agreement brings hope",
    "source": "manual",
    "region": "Europe"
}

Chaque titre est envoyé au backend :

http://127.0.0.1:3000/analyze
Lancement

Les services Docker doivent déjà être lancés :

docker compose up --build

Puis, depuis la racine du projet :

python scraper/manual_collector.py

Si l’environnement Python utilisé est celui de ai-service :

.\ai-service\.venv\Scripts\python.exe scraper/manual_collector.py
Pourquoi un collecteur manuel ?

Le collecteur manuel permet de tester tout le pipeline sans dépendre :

d’un site externe ;
d’un flux RSS instable ;
d’une connexion à une API payante ;
de règles de scraping propres à chaque site.

Il permet de valider la chaîne technique :

collecte
→ prédiction
→ stockage
→ statistiques
→ dashboard
Améliorations futures

Le collecteur pourra évoluer vers :

un lecteur de flux RSS ;
une intégration avec une API d’actualité ;
un scraper respectant les fichiers robots.txt ;
une collecte planifiée ;
une détection automatique des régions ;
une déduplication des titres.

---

## `database/README.md`

```markdown
# Database

Ce dossier contient le script d’initialisation PostgreSQL du projet ASG.

## Rôle

La base PostgreSQL stocke les titres analysés par le système.

Elle permet ensuite :

- d’historiser les prédictions ;
- de récupérer les derniers titres ;
- de calculer des statistiques par région ;
- d’alimenter le dashboard.

## Fichier principal

```text
database/
└── init.sql
Table principale

La table utilisée est :

headlines

Elle contient les colonnes suivantes :

id
title
sentiment
confidence
source
region
created_at
Description des colonnes
id

Identifiant unique du titre.

title

Titre d’actualité analysé.

sentiment

Sentiment prédit par le modèle.

Valeurs possibles :

positive
neutral
negative
confidence

Confiance du modèle pour la classe prédite.

source

Origine du titre.

Exemple :

manual
region

Région géographique associée au titre.

Exemples :

Europe
Middle East
Africa
created_at

Date et heure d’insertion dans la base.

Initialisation avec Docker

La base est lancée via Docker Compose.

Le fichier init.sql est monté dans le conteneur PostgreSQL :

./database/init.sql:/docker-entrypoint-initdb.d/init.sql

Au premier démarrage, PostgreSQL exécute automatiquement ce fichier.

Commandes utiles

Entrer dans PostgreSQL :

docker exec -it asg-postgres psql -U postgres -d asg

Voir les tables :

\dt

Voir les titres sauvegardés :

SELECT * FROM headlines;

Quitter PostgreSQL :

\q
Remarque sur les volumes Docker

Si le volume PostgreSQL existe déjà, init.sql ne sera pas rejoué automatiquement.

Pour repartir de zéro :

docker compose down -v
docker compose up --build

Attention : cette commande supprime les données existantes.


---

## `experiments/README.md`

```markdown
# Experiments

Ce dossier contient les fichiers de démonstration utilisés pendant la construction progressive du projet.

Ils servent à comprendre les briques fondamentales avant d’arriver au code final.

## Rôle du dossier

Les fichiers de ce dossier ne sont pas indispensables au fonctionnement final de l’application.

Ils documentent le chemin d’apprentissage :

```text
tenseurs
→ tokenisation
→ vocabulaire
→ padding
→ embeddings
→ classifieur
→ entraînement

Ils sont utiles pour expliquer en entretien comment le projet a été construit étape par étape.

Exemples de fichiers

Selon l’état du projet, ce dossier peut contenir :

tensor_demo.py
text_processing.py
vocab_demo.py
tensor_text_demo.py
embedding_demo.py
classifier_demo.py
training_step_demo.py
training_loop_demo.py
Objectif pédagogique de chaque étape
tensor_demo.py

Montre comment créer et manipuler un tenseur PyTorch.

Concepts associés :

tenseur ;
shape ;
type de données ;
opérations élément par élément.
text_processing.py

Montre comment transformer un texte brut en tokens.

Exemple :

Peace talks resume

devient :

["peace", "talks", "resume"]
vocab_demo.py

Montre comment construire un vocabulaire.

Exemple :

{
  "<PAD>": 0,
  "<UNK>": 1,
  "peace": 2,
  "talks": 3
}
tensor_text_demo.py

Montre comment transformer des phrases encodées en tenseurs PyTorch.

Exemple de shape :

[batch_size, sequence_length]
embedding_demo.py

Montre comment utiliser une couche :

nn.Embedding

Elle transforme des identifiants de mots en vecteurs denses.

classifier_demo.py

Montre un premier classifieur simple :

Embedding
→ moyenne
→ couche linéaire
→ logits
training_step_demo.py

Montre une seule étape d’entraînement PyTorch :

optimizer.zero_grad()
logits = model(input_ids)
loss = criterion(logits, y_true)
loss.backward()
optimizer.step()
training_loop_demo.py

Montre une boucle d’entraînement sur plusieurs epochs.

Objectif :

observer la loss diminuer progressivement
Pourquoi conserver ces fichiers ?

Ils permettent de montrer que le projet n’a pas été construit comme une boîte noire.

Chaque concept a été isolé, testé et compris avant d’être intégré dans le service final.

Cela aide à expliquer :

ce qu’est un tenseur ;
pourquoi il faut tokeniser ;
pourquoi il faut un vocabulaire ;
pourquoi le padding est nécessaire ;
ce qu’est une couche d’embedding ;
comment fonctionne une boucle d’entraînement PyTorch.
Différence avec le code final

Le code final utilisé par l’application se trouve principalement dans :

ai-service/

Le dossier experiments/ sert de support pédagogique et historique.

Il n’est pas appelé par Docker Compose.