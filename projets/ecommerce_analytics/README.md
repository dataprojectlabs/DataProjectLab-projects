# E-Commerce Analytics 360

> Analyse complète d'une plateforme e-commerce africaine : performance commerciale, nettoyage de données, segmentation RFM et dashboard Power BI.

**Niveau** : Intermédiaire / Avancé · **Durée** : 10h à 14h · **Outils** : Python, DuckDB, Power BI

---

## Étapes du projet

| # | Étape | Outils | Notebook |
|---|---|---|---|
| 1 | Contexte métier & exploration des données | Python, pandas | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dataprojectlabs/DataProjectLab-projects/blob/main/projets/ecommerce_analytics/enonce/nb1_exploration.ipynb) |
| 2 | Data Cleaning & Feature Engineering | Python, pandas, sqlalchemy | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dataprojectlabs/DataProjectLab-projects/blob/main/projets/ecommerce_analytics/enonce/nb2_data_cleaning.ipynb) |
| 3 | SQL Analytics, KPIs & Segmentation RFM | Python, DuckDB, matplotlib | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dataprojectlabs/DataProjectLab-projects/blob/main/projets/ecommerce_analytics/enonce/nb3_sql_rfm.ipynb) |
| 4 | Power BI Design Guide | Power BI Desktop | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dataprojectlabs/DataProjectLab-projects/blob/main/projets/ecommerce_analytics/enonce/nb4_powerbi.ipynb) |



---

## Données

Les datasets sont dans le dossier [`data/`](./data/).

| Fichier | Description |
|---|---|
| `customers.csv` | Clients (id, pays, ville, segment, date inscription) |
| `products.csv` | Catalogue produits (id, nom, catégorie, marque, prix, coût) |
| `orders.csv` | Commandes (id, client, date, canal, statut, montant) |
| `order_items.csv` | Lignes de commande (order_id, product_id, quantité, prix) |
| `reviews.csv` | Avis clients (note 1-5, commentaire, date) |
| `web_logs.csv` | Comportement web (sessions, pages, device) |
| `social_media.csv` | Publications réseaux sociaux (engagement, plateforme) |

---

## Prérequis techniques

- Compte Google (pour Colab)
- Power BI Desktop (étape 4) — [téléchargement gratuit](https://powerbi.microsoft.com/fr-fr/desktop/)
- Aucune installation Python requise (tout tourne dans Colab)

---

## Contexte business

Tu es **Data Analyst** chez **ShopAfrica+**, une plateforme e-commerce opérant en Afrique et en Europe. Le Directeur Général souhaite une vision claire de la performance : produits, clients, canaux, satisfaction.

Le contexte complet et le brief métier sont disponibles sur la [plateforme DataProjectLab](https://dataprojectlab.com).
