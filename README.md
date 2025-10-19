# 🧠 Retail Data POC – PostgreSQL + dbt + Flask + Docker

## 🎯 Objectif

Ce projet met en place une architecture **data moderne** avec :
- **PostgreSQL** pour stocker les données,
- **Python (Loader)** pour générer des données factices (transactions e-commerce),
- **dbt** pour transformer les données (ELT),
- **Flask** pour exposer les indicateurs via une API REST,
- **Docker Compose** pour tout automatiser.

---
## 📂 Structure du projet

```
retail-poc/
├── docker-compose.yml
├── loader/              → Génère et charge les données
├── dbt/                 → Transformations dbt
├── flask_api/           → API Flask
└── README.md
```
## 🐳 Services Docker
Service	| Rôle | Port |
|----------|--------------|------|
postgres | Base de données PostgreSQL | 5433 |
loader | Génère et charge 500 000 transactions | - |
dbt |	Transforme les données dans PostgreSQL | - |
flask |	API REST pour exposer les indicateurs |	5000 |
## 🚀 Lancer le projet
1️⃣ Construire et démarrer les conteneurs
    ` docker-compose up -d --build `
## ✅ Vérification
Voir les conteneurs actifs
` docker ps `

## Vérifier l’API

Ouvrir dans le navigateur :
👉 http://localhost:5000/health

Résultat attendu :

``` {"status": "ok"} ```

## 📊 Endpoints disponibles
Endpoint	Description	Exemple
 - /health Vérifie la connexion à la base	/health
 - /api/users/<user_id>/orders_count Nombre de commandes d’un utilisateur
 - /api/users/<user_id>/summary	Résumé des commandes d’un utilisateur
 - /api/sales/by_month	Total des ventes par mois

## 🔧 Commandes utiles
| Action |	Commande |
|----------|--------------|
| Arrêter tous les conteneurs |	` docker-compose down ` |
| Voir les logs Flask |	` docker logs -f retail-poc-flask ` |
| Voir les logs dbt |	` docker logs -f retail-poc-dbt ` |
| Ouvrir PostgreSQL |	` docker exec -it retail-poc-postgres psql -U demo -d demo`  |

## 👨‍💻 Auteur

Ghilene Mohamed Omar
Étudiant en Data Science — Alternant
🔗 www.linkedin.com/in/mohamed-omar-ghilene


---
