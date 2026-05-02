# Backend TypeScript

Ce dossier contient le backend NodeJS / TypeScript du projet **ASG - Analyseur de Sentiments Géopolitiques**.

Il sert d’intermédiaire entre :

- le client ou le dashboard ;
- le microservice Python FastAPI ;
- la base PostgreSQL.

## Rôle dans l’architecture

Le backend reçoit les titres à analyser, appelle le service IA, sauvegarde les résultats en base, puis expose les données nécessaires au dashboard.

```text
Client / Dashboard
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
PostgreSQL avec pg
Docker
Structure principale
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
