# Scraper / Collecteur

Ce dossier contient le collecteur de titres du projet **ASG**.

Pour l’instant, ce n’est pas un vrai scraper web : c’est un collecteur manuel qui envoie des titres prédéfinis au backend.

## Rôle

Le collecteur teste le pipeline complet :

```text
titre
→ backend TypeScript
→ modèle IA Python
→ PostgreSQL
→ dashboard
Fichier principal
scraper/
└── manual_collector.py
Lancement

Les services doivent d’abord être lancés :

docker compose up --build

Puis, depuis la racine du projet :

python scraper/manual_collector.py

Ou avec l’environnement Python du service IA :

.\ai-service\.venv\Scripts\python.exe scraper/manual_collector.py
Améliorations possibles
utiliser des flux RSS ;
connecter une API d’actualité ;
éviter les doublons ;
détecter automatiquement la région ;
planifier une collecte régulière.