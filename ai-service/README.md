# AI Service

Ce dossier contient le microservice d’intelligence artificielle du projet **ASG - Analyseur de Sentiments Géopolitiques**.

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

Fichiers principaux : 
ai-service/
├── app.py
├── model.py
├── train.py
├── predict.py
├── data.csv
├── requirements.txt
├── Dockerfile
└── README.md

Modèle PyTorch

Le fichier model.py contient la classe SentimentClassifier.

Le modèle suit cette architecture :

Embedding
→ moyenne des embeddings
→ couche linéaire
→ ReLU
→ couche linéaire
→ logits