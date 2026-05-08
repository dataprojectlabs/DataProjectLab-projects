# Ressources Power BI — E-Commerce Analytics 360

> Guide de référence complet pour la création du dashboard Power BI **ShopAfrica+** (5 pages + page DAX) — destiné à servir de support pour la vidéo tutoriel.

---

## Sommaire

1. [Contexte du projet](#1-contexte-du-projet)
2. [Sources de données](#2-sources-de-données)
3. [Charte graphique](#3-charte-graphique)
4. [Étape 1 — Import des données](#étape-1--import-des-données-dans-power-bi)
5. [Étape 2 — Désactiver Auto Date/Time](#étape-2--désactiver-auto-datetime)
6. [Étape 3 — Modèle de données (relations)](#étape-3--modèle-de-données-relations)
7. [Étape 4 — Table Calendrier](#étape-4--table-calendrier)
8. [Étape 5 — Table _Mesures](#étape-5--table-_mesures)
9. [Étape 6 — Mesures DAX (48 mesures)](#étape-6--mesures-dax-48-mesures)
10. [Étape 7 — Backgrounds & navigation](#étape-7--backgrounds--navigation)
11. [Étape 8 — Construction des 5 pages](#étape-8--construction-des-5-pages)
12. [Étape 9 — Validation finale](#étape-9--validation-finale)
13. [Annexes](#annexes)

---

## 1. Contexte du projet

| Champ | Valeur |
|---|---|
| **Projet** | E-Commerce Analytics 360 |
| **Client fictif** | ShopAfrica+ |
| **Décideur** | M. Diallo, Directeur |
| **Période d'analyse** | janvier — décembre 2024 |
| **Niveau** | Avancé |
| **Outils** | Power BI Desktop |
| **Durée estimée** | 6h à 8h |

**Objectif business :** Transformer les données SQL en un dashboard décisionnel **5 pages** permettant à M. Diallo de piloter la performance commerciale, les produits, les clients, le funnel digital et la satisfaction.

**Question finale à laquelle le dashboard doit répondre :**

> *"Que doit faire ShopAfrica+ dans les 3 prochains mois ?"*

---

## 2. Sources de données

7 fichiers CSV hébergés sur GitHub à importer en mode **Web → URL** dans Power BI.

| Fichier | URL | Rôle | Lignes attendues |
|---|---|---|---|
| `dim_customers` | `https://raw.githubusercontent.com/dataprojectlabs/DataProjectLab-projects/refs/heads/main/projets/ecommerce_analytics/corrige/outputs/dim_customers.csv` | Dimension clients | 3 000 |
| `dim_products` | `https://raw.githubusercontent.com/dataprojectlabs/DataProjectLab-projects/refs/heads/main/projets/ecommerce_analytics/corrige/outputs/dim_products.csv` | Dimension produits | 30 |
| `fact_orders` | `https://raw.githubusercontent.com/dataprojectlabs/DataProjectLab-projects/refs/heads/main/projets/ecommerce_analytics/corrige/outputs/fact_orders.csv` | Commandes | ~16 000 |
| `fact_order_items` | `https://raw.githubusercontent.com/dataprojectlabs/DataProjectLab-projects/refs/heads/main/projets/ecommerce_analytics/corrige/outputs/fact_order_items.csv` | Lignes de commande | ~40 000 |
| `fact_reviews` | `https://raw.githubusercontent.com/dataprojectlabs/DataProjectLab-projects/refs/heads/main/projets/ecommerce_analytics/corrige/outputs/fact_reviews.csv` | Avis clients | ~3 000 |
| `fact_web_logs` | `https://raw.githubusercontent.com/dataprojectlabs/DataProjectLab-projects/refs/heads/main/projets/ecommerce_analytics/corrige/outputs/fact_web_logs.csv` | Sessions web | ~6 000 |
| `clients_rfm_segments` | `https://raw.githubusercontent.com/dataprojectlabs/DataProjectLab-projects/refs/heads/main/projets/ecommerce_analytics/corrige/outputs/clients_rfm_segments.csv` | Segmentation RFM | 3 000 |

**Schéma simplifié des tables :**

```
                          Calendrier (dim temps)
                                  |
                                  v
        dim_customers --> fact_orders --> fact_order_items <-- dim_products
              |                |                  |
              |                v                  v
              +---------> fact_reviews ----+
              |                |
              +---------> fact_web_logs ---+
              |
              +---------> clients_rfm_segments
```

---

## 3. Charte graphique

### Palette principale (e-commerce)

| Usage | Hex | Aperçu |
|---|---|---|
| Fond principal | `#1A1F2E` | Navy foncé |
| Fond secondaire (cartes) | `#232836` | Navy moyen |
| Accent principal | `#3B82F6` | Bleu |
| Performance positive | `#10B981` | Vert teal |
| Accent secondaire | `#8B5CF6` | Violet |
| Attention | `#F59E0B` | Orange |
| Alerte | `#EF4444` | Rouge |
| Indigo (variations) | `#6366F1` | Indigo |
| Texte principal | `#FFFFFF` | Blanc |
| Texte secondaire | `#E8E8E8` | Gris clair |
| Texte discret | `#888888` | Gris moyen |

### Sémantique des couleurs (immuable)

| Couleur | Signification |
|---|---|
| Rouge `#EF4444` | Alerte / agir aujourd'hui |
| Orange `#F59E0B` | Attention / cette semaine |
| Vert `#10B981` | OK / aucune action |

### Couleur dédiée par KPI Overview

| KPI | Couleur |
|---|---|
| CA | Bleu `#3B82F6` |
| Marge | Vert `#10B981` |
| Commandes | Teal `#14B8A6` |
| Clients | Violet `#8B5CF6` |
| Panier | Orange `#F59E0B` |
| Note | Rouge `#EF4444` |

### Palette segments RFM

| Segment | Couleur |
|---|---|
| Champions | `#10B981` |
| Fidèles | `#8B5CF6` |
| Gros dépensiers occasionnels | `#F59E0B` |
| Nouveaux prometteurs | `#3B82F6` |
| À réactiver | `#EF4444` |
| Dormants | `#888888` |

### Typographie

| Usage | Police | Taille |
|---|---|---|
| Titres pages | Segoe UI bold | 22-26 px |
| Sous-titres | Segoe UI regular | 13-14 px |
| Valeurs KPI | Segoe UI bold | 34-42 px |
| Labels KPI | Segoe UI regular | 12-13 px |
| Variations (pastilles) | Segoe UI | 11 px |

---

## Étape 1 — Import des données dans Power BI

1. Ouvrir **Power BI Desktop**
2. Accueil → **Obtenir des données → Web**
3. Coller l'URL du premier fichier (par exemple `dim_customers.csv`)
4. Power BI détecte le CSV → cliquer **Charger** ou **Transformer les données** pour vérifier les types
5. Répéter pour les **7 fichiers** de la section précédente

**Vérification des types après import** (à faire en Power Query) :

| Table | Colonne | Type attendu |
|---|---|---|
| `fact_orders` | `order_date` | DateTime |
| `fact_orders` | `montant_total` | Décimal |
| `fact_orders` | `delivery_delay` | Nombre entier |
| `fact_order_items` | `quantite` | Nombre entier |
| `fact_order_items` | `prix_unitaire`, `line_revenue`, `line_cost`, `line_margin` | Décimal |
| `fact_reviews` | `rating` | Nombre entier |
| `fact_reviews` | `date_review` | DateTime |
| `fact_web_logs` | `timestamp` | DateTime |
| `clients_rfm_segments` | `frequency`, `recency`, `R_score`, `F_score`, `M_score` | Nombre entier |

Cliquer **Fermer & appliquer** pour charger les 7 tables.

---

## Étape 2 — Désactiver Auto Date/Time

**Obligatoire AVANT de modéliser**.

`Fichier → Options et paramètres → Options → Chargement des données (Fichier actuel)` → **décocher** *"Date/heure automatique pour le fichier actuel"*.

Pourquoi : sans cette étape, Power BI crée 5 à 10 tables `LocalDateTable_*` parasites qui polluent le modèle, perturbent les relations et empêchent certaines mesures `SAMEPERIODLASTYEAR` de fonctionner correctement.

---

## Étape 3 — Modèle de données (relations)

Schéma en étoile à construire dans **Affichage du modèle**.

### 10 relations à créer

| De | Colonne | Vers | Colonne | Cardinalité | Direction |
|---|---|---|---|---|---|
| `fact_orders` | `customer_id` | `dim_customers` | `customer_id` | Many → One | Single |
| `fact_reviews` | `customer_id` | `dim_customers` | `customer_id` | Many → One | Single |
| `fact_web_logs` | `customer_id` | `dim_customers` | `customer_id` | Many → One | Single |
| `clients_rfm_segments` | `customer_id` | `dim_customers` | `customer_id` | Many → One | Single |
| `fact_order_items` | `order_id` | `fact_orders` | `order_id` | Many → One | Single |
| `fact_order_items` | `product_id` | `dim_products` | `product_id` | Many → One | Single |
| `fact_reviews` | `order_id` | `fact_orders` | `order_id` | Many → One | Single |
| `fact_reviews` | `product_id` | `dim_products` | `product_id` | Many → One | Single |
| `fact_orders` | `order_date` | `Calendrier` | `Date` | Many → One | Single |
| `fact_web_logs` | `session_date` | `Calendrier` | `Date` | Many → One | Single |

⚠️ Vérifier qu'**aucune relation M:M bidirectionnelle** n'est créée et qu'il n'y a aucun chemin ambigu.

⚠️ La colonne `fact_web_logs[session_date]` est une **colonne calculée** à créer (voir étape suivante) car `timestamp` est en DateTime.

---

## Étape 4 — Table Calendrier

### 4.1 — Créer la colonne calculée `session_date`

Dans le panneau Données → clic droit sur `fact_web_logs` → **Nouvelle colonne** :

```dax
session_date = DATE(YEAR([timestamp]), MONTH([timestamp]), DAY([timestamp]))
```

### 4.2 — Créer la table Calendrier

Modélisation → **Nouvelle table** → coller :

```dax
Calendrier =
ADDCOLUMNS(
    CALENDAR(DATE(2022,1,1), DATE(2024,12,31)),
    "Annee",        YEAR([Date]),
    "Mois_Num",     MONTH([Date]),
    "Mois_Nom",     FORMAT([Date], "MMMM", "fr-FR"),
    "Trimestre",    "T" & QUARTER([Date]),
    "Semaine",      WEEKNUM([Date]),
    "Jour_Semaine", FORMAT([Date], "dddd", "fr-FR"),
    "Est_Weekend",  IF(WEEKDAY([Date],2) >= 6, 1, 0),
    "Annee_Mois",   FORMAT([Date], "YYYY-MM")
)
```

### 4.3 — Marquer comme table de dates

Clic droit sur la table `Calendrier` dans le panneau Données → **Marquer comme table de dates** → choisir la colonne `Date` → OK.

---

## Étape 5 — Table _Mesures

Modélisation → **Nouvelle table** → coller :

```dax
_Mesures = {BLANK()}
```

Puis dans le panneau Champs → clic droit sur la colonne `Value` → **Masquer**.

La table sert uniquement de conteneur pour héberger les 48 mesures dans des dossiers d'affichage.

---

## Étape 6 — Mesures DAX (48 mesures)

Toutes les mesures sont créées dans la table `_Mesures` et organisées par **dossier d'affichage** (propriété "Display Folder" dans Power BI).

### Récapitulatif

| # | Dossier | Nb mesures |
|---|---|---|
| 1 | `01 KPIs de base` | 9 |
| 2 | `02 KPIs avances` | 6 |
| 3 | `03 Variations vs N-1` | 6 |
| 4 | `04 Couleurs Variation` | 6 |
| 5 | `05 Segment RFM` | 1 |
| 6 | `06 Funnel digital` | 10 |
| 7 | `07 Segment Produits` | 4 |
| 8 | `08 Sous-titres dynamiques` | 6 |
|  | **Total** | **48** |

---

### 📂 Dossier 01 — KPIs de base (9 mesures)

```dax
CA Total =
CALCULATE(
    SUM(fact_order_items[line_revenue]),
    fact_orders[order_status] = "Livree"
)

Marge Totale =
CALCULATE(
    SUM(fact_order_items[line_margin]),
    fact_orders[order_status] = "Livree"
)

Taux de Marge =
DIVIDE([Marge Totale], [CA Total], 0)

Nb Commandes =
CALCULATE(
    DISTINCTCOUNT(fact_orders[order_id]),
    fact_orders[order_status] = "Livree"
)

Nb Clients =
DISTINCTCOUNT(dim_customers[customer_id])

Panier Moyen =
DIVIDE([CA Total], [Nb Commandes], 0)

Quantite Vendue =
CALCULATE(
    SUM(fact_order_items[quantite]),
    fact_orders[order_status] = "Livree"
)

Note Moyenne =
AVERAGE(fact_reviews[rating])

Nb Avis =
COUNTROWS(fact_reviews)
```

**Format strings recommandés :**
- `CA Total`, `Marge Totale`, `Panier Moyen` → `#,0" €"`
- `Taux de Marge` → `0.0%`
- `Nb Commandes`, `Nb Clients`, `Quantite Vendue`, `Nb Avis` → `#,0`
- `Note Moyenne` → `0.0`

---

### 📂 Dossier 02 — KPIs avancés (6 mesures)

```dax
Nb Produits Actifs =
CALCULATE(
    DISTINCTCOUNT(fact_order_items[product_id]),
    fact_order_items[quantite] > 0
)

CA Moyen par Client =
DIVIDE([CA Total], [Nb Clients], 0)

Nb Commandes par Client =
DIVIDE([Nb Commandes], [Nb Clients], 0)

Nb Produits Note <3 =
CALCULATE(
    DISTINCTCOUNT(fact_reviews[product_id]),
    FILTER(
        VALUES(fact_reviews[product_id]),
        CALCULATE(AVERAGE(fact_reviews[rating])) < 3
    )
)

Pct Avis Positifs =
DIVIDE(
    CALCULATE(COUNTROWS(fact_reviews), fact_reviews[rating] >= 4),
    [Nb Avis],
    0
)

Tendance Note =
VAR _na = [Note Moyenne]
VAR _np = CALCULATE([Note Moyenne], DATEADD(Calendrier[Date], -1, MONTH))
VAR _delta = _na - _np
RETURN
    SWITCH(
        TRUE(),
        _delta > 0.1, UNICHAR(9650) & " +" & FORMAT(_delta, "0.0"),
        _delta < -0.1, UNICHAR(9660) & " " & FORMAT(_delta, "0.0"),
        UNICHAR(8594) & " stable"
    )
```

---

### 📂 Dossier 03 — Variations vs N-1 (6 mesures)

Pattern récurrent : `CALCULATE([Mesure], SAMEPERIODLASTYEAR(Calendrier[Date]))` puis pastille avec flèche `▲ ▼` via `UNICHAR(9650)` / `UNICHAR(9660)`.

```dax
Variation CA % =
VAR _a = [CA Total]
VAR _p = CALCULATE([CA Total], SAMEPERIODLASTYEAR(Calendrier[Date]))
VAR _pct = DIVIDE(_a - _p, _p, 0)
VAR _f = FORMAT(_pct, "0.0%;0.0%")
RETURN IF(_pct > 0, UNICHAR(9650) & " " & _f, UNICHAR(9660) & " " & _f)

Variation Marge % =
VAR _a = [Marge Totale]
VAR _p = CALCULATE([Marge Totale], SAMEPERIODLASTYEAR(Calendrier[Date]))
VAR _pct = DIVIDE(_a - _p, _p, 0)
VAR _f = FORMAT(_pct, "0.0%;0.0%")
RETURN IF(_pct > 0, UNICHAR(9650) & " " & _f, UNICHAR(9660) & " " & _f)

Variation Commandes % =
VAR _a = [Nb Commandes]
VAR _p = CALCULATE([Nb Commandes], SAMEPERIODLASTYEAR(Calendrier[Date]))
VAR _pct = DIVIDE(_a - _p, _p, 0)
VAR _f = FORMAT(_pct, "0.0%;0.0%")
RETURN IF(_pct > 0, UNICHAR(9650) & " " & _f, UNICHAR(9660) & " " & _f)

Variation Clients % =
VAR _a = [Nb Clients]
VAR _p = CALCULATE([Nb Clients], SAMEPERIODLASTYEAR(Calendrier[Date]))
VAR _pct = DIVIDE(_a - _p, _p, 0)
VAR _f = FORMAT(_pct, "0.0%;0.0%")
RETURN IF(_pct > 0, UNICHAR(9650) & " " & _f, UNICHAR(9660) & " " & _f)

Variation Panier % =
VAR _a = [Panier Moyen]
VAR _p = CALCULATE([Panier Moyen], SAMEPERIODLASTYEAR(Calendrier[Date]))
VAR _pct = DIVIDE(_a - _p, _p, 0)
VAR _f = FORMAT(_pct, "0.0%;0.0%")
RETURN IF(_pct > 0, UNICHAR(9650) & " " & _f, UNICHAR(9660) & " " & _f)

Variation Note =
VAR _a = [Note Moyenne]
VAR _p = CALCULATE([Note Moyenne], SAMEPERIODLASTYEAR(Calendrier[Date]))
VAR _d = _a - _p
RETURN IF(_d > 0, UNICHAR(9650) & " +" & FORMAT(_d, "0.0"), UNICHAR(9660) & " " & FORMAT(_d, "0.0"))
```

---

### 📂 Dossier 04 — Couleurs Variation (6 mesures)

À utiliser pour le **formatage conditionnel** des cartes KPI : Format → Couleur d'arrière-plan → **Par formule** → choisir la mesure correspondante.

```dax
Couleur Variation CA =
VAR _p = DIVIDE(
    [CA Total] - CALCULATE([CA Total], SAMEPERIODLASTYEAR(Calendrier[Date])),
    CALCULATE([CA Total], SAMEPERIODLASTYEAR(Calendrier[Date])),
    0
)
RETURN SWITCH(TRUE(), _p > 0, "#10B981", _p < 0, "#EF4444", "#888888")

-- Même pattern pour les 5 autres : Marge, Commandes, Clients, Panier, Note
-- (remplacer la mesure de référence dans les 2 endroits)
```

---

### 📂 Dossier 05 — Segment RFM (1 mesure)

```dax
Couleur Segment RFM =
SWITCH(
    SELECTEDVALUE(clients_rfm_segments[segment_rfm]),
    "Champions",                    "#10B981",
    "Fidèles",                      "#8B5CF6",
    "Gros dépensiers occasionnels", "#F59E0B",
    "Nouveaux prometteurs",         "#3B82F6",
    "À réactiver",                  "#EF4444",
    "Dormants",                     "#888888",
    "#888888"
)
```

---

### 📂 Dossier 06 — Funnel digital (10 mesures)

```dax
Nb Sessions =
DISTINCTCOUNT(fact_web_logs[session_id])

Nb Vues =
CALCULATE(
    COUNTROWS(fact_web_logs),
    SEARCH("fiche_produit", fact_web_logs[page], 1, 0) > 0
)

Nb Ajouts Panier =
CALCULATE(
    DISTINCTCOUNT(fact_web_logs[session_id]),
    SEARCH("panier", fact_web_logs[page], 1, 0) > 0
)

Nb Checkout =
CALCULATE(
    DISTINCTCOUNT(fact_web_logs[session_id]),
    SEARCH("checkout", fact_web_logs[page], 1, 0) > 0
)

Nb Achats =
CALCULATE(
    DISTINCTCOUNT(fact_web_logs[session_id]),
    SEARCH("confirmation", fact_web_logs[page], 1, 0) > 0
)

Taux Conversion =
DIVIDE([Nb Achats], [Nb Vues], 0)

Taux Panier sur Vues =
DIVIDE([Nb Ajouts Panier], [Nb Vues], 0)

Taux Checkout sur Panier =
DIVIDE([Nb Checkout], [Nb Ajouts Panier], 0)

Taux Achat sur Checkout =
DIVIDE([Nb Achats], [Nb Checkout], 0)

Abandon Vues vers Panier =
VAR _ab = 1 - [Taux Panier sur Vues]
RETURN "Perte majeure entre Vues et Panier - " & FORMAT(_ab, "0.0%") & " d'abandons"
```

`Abandon Vues vers Panier` génère le texte de l'encadré rouge "Point de friction" en bas du visuel funnel.

---

### 📂 Dossier 07 — Segment Produits (4 mesures)

```dax
CA Produit =
CALCULATE(
    SUM(fact_order_items[line_revenue]),
    fact_orders[order_status] = "Livree"
)

Marge Produit =
CALCULATE(
    SUM(fact_order_items[line_margin]),
    fact_orders[order_status] = "Livree"
)

Taux de Marge Produit =
DIVIDE([Marge Produit], [CA Produit], 0)

Note Moyenne Produit =
CALCULATE(
    AVERAGE(fact_reviews[rating]),
    ALLEXCEPT(fact_reviews, fact_reviews[product_id])
)
```

L'usage d'`ALLEXCEPT` sur `Note Moyenne Produit` permet d'afficher la note de chaque produit indépendamment du contexte de filtre (utile pour les visuels Top 10 / Bottom 4).

---

### 📂 Dossier 08 — Sous-titres dynamiques (6 mesures)

Cette série permet d'afficher un sous-titre qui s'adapte automatiquement aux filtres `Année` et `Trimestre` sélectionnés. Tous les sous-titres réutilisent la même mesure helper `Periode Active`.

```dax
Periode Active =
VAR _ya = MIN(Calendrier[Annee])
VAR _yz = MAX(Calendrier[Annee])
VAR _ma = MIN(Calendrier[Mois_Num])
VAR _mz = MAX(Calendrier[Mois_Num])
VAR _maName =
    SWITCH(_ma,
        1, "janv", 2, "fev", 3, "mars", 4, "avr",
        5, "mai", 6, "juin", 7, "juil", 8, "aou",
        9, "sept", 10, "oct", 11, "nov", 12, "dec")
VAR _mzName =
    SWITCH(_mz,
        1, "janv", 2, "fev", 3, "mars", 4, "avr",
        5, "mai", 6, "juin", 7, "juil", 8, "aou",
        9, "sept", 10, "oct", 11, "nov", 12, "dec")
RETURN
    SWITCH(TRUE(),
        _ya <> _yz, _ya & " " & UNICHAR(8212) & " " & _yz,
        _ma = _mz, _maName & " " & _ya,
        _ma = 1 && _mz = 12, "janv " & UNICHAR(8212) & " dec " & _ya,
        _maName & " " & UNICHAR(8212) & " " & _mzName & " " & _ya
    )

Sous-titre Overview =
"Performance globale  ·  " & [Periode Active]

Sous-titre Produits =
"Performance & Rentabilite  ·  " & [Periode Active]

Sous-titre Clients =
"Segmentation & Valeur  ·  " & [Periode Active]

Sous-titre Funnel =
"Analyse du tunnel d'achat  ·  " & [Periode Active]

Sous-titre Satisfaction =
"Avis & notes produits  ·  " & [Periode Active]
```

**Comportement attendu :**

| Filtres | `Periode Active` |
|---|---|
| Aucun filtre | `2022 — 2024` |
| Année = 2024 + tous les trimestres | `janv — dec 2024` |
| Année = 2024 + T2 et T3 sélectionnés | `avr — sept 2024` |
| Année = 2024 + T1 uniquement | `janv — mars 2024` |
| Année = 2023 et 2024 | `2023 — 2024` |

**Utilisation :** insérer une zone de texte sur chaque page, et y placer **un visuel "Carte"** lié à la mesure `Sous-titre <Page>`. Configurer la mise en forme : taille 13 px, gris `#888888`, alignement à gauche.

---

## Étape 7 — Backgrounds & navigation

### 7.1 — Backgrounds

Le projet inclut un fichier **`mockup_ecommerce_powerbi.pptx`** avec 6 slides (5 pages dashboard + page DAX). Chaque slide est exportée en **PNG vierge** depuis PowerPoint :

`Fichier → Exporter → Modifier le type de fichier → PNG`

Les PNG vierges sont importés comme **arrière-plan de page** dans Power BI :

`Format de la page → Arrière-plan de page → Image → Parcourir → choisir le PNG → Ajustement: Ajuster`

Cela donne instantanément le look navy professionnel avec sidebar, accent borders et zones blanches positionnées correctement. Il ne reste plus qu'à poser les visuels Power BI dans les zones vides.

### 7.2 — Navigation entre les pages

Pour chaque item de la sidebar (Overview, Produit, Clients, Funnel digital, Satisfaction) :
- Insertion → **Bouton transparent**
- Le positionner exactement sur la zone de l'item dans le PNG
- Format → Action → **Type : Navigation de page** → sélectionner la page cible
- Maintenir Ctrl + clic pour tester

**Astuce :** dupliquer la page une fois construite, puis adapter chaque copie pour les autres pages. La sidebar reste identique.

### 7.3 — Slicers globaux

Sur les 5 pages dashboard, ajouter en haut à droite :

| Slicer | Champ | Style |
|---|---|---|
| Année | `Calendrier[Annee]` | **Boutons** (single select), valeurs `2022` / `2023` / `2024` |
| Trimestre | `Calendrier[Trimestre]` | **Boutons** (multi-select), valeurs `T1` / `T2` / `T3` / `T4` |

**Style boutons :** forme arrondie (border-radius 20px), bordure bleue `#3B82F6`, fond transparent ; bouton actif → fond bleu, texte blanc ; bouton inactif → texte bleu, fond transparent.

**Synchronisation :** clic droit sur chaque slicer → **Synchroniser les segments** → cocher les 5 pages (visible **et** filtre).

---

## Étape 8 — Construction des 5 pages

### Page 1 — Overview

**Titre :** `Overview`
**Sous-titre :** mesure `Sous-titre Overview` (`"Performance globale · janv — dec 2024"`)

**Layout :**

```
┌─────┬──────┬──────┬──────┬──────┬──────┐
│ KPI │ KPI  │ KPI  │ KPI  │ KPI  │ KPI  │ ← 6 cards
└─────┴──────┴──────┴──────┴──────┴──────┘
┌─────────────────────────┬──────────────┐
│  Evolution CA 2024      │  Donut       │
│  (Aires)                │  catégories  │
└─────────────────────────┴──────────────┘
┌──────────────┬──────────────────────────┐
│  Bar canal   │  Donut paiement         │
└──────────────┴──────────────────────────┘
```

**6 KPIs (top row) :**

| Card | Mesure valeur | Mesure variation | Couleur accent |
|---|---|---|---|
| Chiffre d'affaires | `CA Total` | `Variation CA %` | `#3B82F6` |
| Marge totale | `Marge Totale` | `Variation Marge %` | `#10B981` |
| Commandes | `Nb Commandes` | `Variation Commandes %` | `#14B8A6` |
| Clients actifs | `Nb Clients` | `Variation Clients %` | `#8B5CF6` |
| Panier moyen | `Panier Moyen` | `Variation Panier %` | `#F59E0B` |
| Note moyenne | `Note Moyenne` | `Variation Note` | `#EF4444` |

Pour chaque card, ajouter le formatage conditionnel sur la pastille variation : `Format → Couleur d'arrière-plan → Par formule → Couleur Variation <KPI>`.

**Visuels (bottom rows) :**

| Visuel | Type | Champs |
|---|---|---|
| Evolution CA | Graphique en aires | Axe X = `Calendrier[Mois_Nom]` (trié par `Mois_Num`), Axe Y = `[CA Total]` |
| CA par catégorie | Anneau | Légende = `dim_products[categorie]`, Valeurs = `[CA Total]` |
| CA par canal | Barre horizontale | Axe Y = `fact_orders[canal]`, Axe X = `[CA Total]` |
| Moyen de paiement | Anneau | Légende = `fact_orders[payment_method]`, Valeurs = `[CA Total]` |

**Valeurs attendues 2024 :**

| KPI | Valeur |
|---|---|
| CA Total | 3,9 M€ (▼ -54,3%) |
| Marge Totale | 1,8 M€ (▼ -54,2%) |
| Nb Commandes | 3 018 (▼ -52,8%) |
| Nb Clients | 3 000 (● 0,0%) |
| Panier Moyen | 1 297 € (▼ -3,1%) |
| Note Moyenne | 3,8 (▼ -0,1) |

---

### Page 2 — Produit

**Titre :** `Produits`
**Sous-titre :** mesure `Sous-titre Produits`

**Layout :**

```
┌──────┬──────┬──────┬──────┐  ← 4 KPIs
│ Qté  │ Rev. │ Marg.│ Prod.│
└──────┴──────┴──────┴──────┘
┌────────────────┬─────────────┐
│ Top 10         │ Scatter     │
│ produits       │ Revenu/Marge│
└────────────────┴─────────────┘
┌──────────────────────────────┐
│ Tableau détail produits      │
└──────────────────────────────┘
```

**4 KPIs :**

| Card | Mesure | Couleur |
|---|---|---|
| Qté vendue | `Quantite Vendue` | `#3B82F6` |
| Revenu produits | `CA Produit` | `#3B82F6` |
| Marge produits | `Marge Produit` | `#10B981` |
| Produits actifs | `Nb Produits Actifs` | `#10B981` |

**Visuels :**

| Visuel | Type | Champs |
|---|---|---|
| Top 10 produits | Barre horizontale (DESC, top N=10) | Axe Y = `dim_products[nom_produit]`, Axe X = `[CA Produit]` |
| Scatter Revenu/Marge | Nuage de points | X = `[CA Produit]`, Y = `[Marge Produit]`, Taille = `[Quantite Vendue]`, Détails = `dim_products[nom_produit]` |
| Tableau détail | Tableau | `nom_produit`, `categorie`, `Quantite Vendue`, `CA Produit`, `Marge Produit`, `Taux de Marge Produit` |

---

### Page 3 — Clients

**Titre :** `Clients`
**Sous-titre :** mesure `Sous-titre Clients`

**Layout :**

```
┌────────┬────────┬────────┐  ← 3 KPIs
│ Clients│ Rev/Cli│ Cmd/Cli│
└────────┴────────┴────────┘
┌────────┬────────┬────────┐  ← 3 charts
│CA seg. │Cmd seg.│Donut   │
│client  │client  │RFM     │
└────────┴────────┴────────┘
┌─────────────────┬──────────┐
│ CA par RFM      │ Top      │
│                 │ clients  │
└─────────────────┴──────────┘
```

**3 KPIs :**

| Card | Mesure | Couleur |
|---|---|---|
| Clients actifs | `Nb Clients` | `#3B82F6` |
| Revenu moy / client | `CA Moyen par Client` | `#3B82F6` |
| Commande moy / client | `Nb Commandes par Client` | `#3B82F6` |

**Visuels :**

| Visuel | Type | Champs |
|---|---|---|
| CA par segment client | Barre | Axe Y = `dim_customers[segment_client]`, Axe X = `[CA Total]` |
| Commandes par segment | Histogramme | Axe X = `dim_customers[segment_client]`, Axe Y = `[Nb Commandes]` |
| Répartition Clients RFM | Anneau | Légende = `clients_rfm_segments[segment_rfm]`, Valeurs = `[Nb Clients]`, **formatage conditionnel couleur via `Couleur Segment RFM`** |
| CA par segment RFM | Barre | Axe Y = `clients_rfm_segments[segment_rfm]`, Axe X = `[CA Total]` |
| Top clients | Tableau (DESC sur revenu) | `customer_id`, `segment_client`, `[CA Total]`, `[Nb Commandes]` |

---

### Page 4 — Funnel digital

**Titre :** `Funnel digital`
**Sous-titre :** mesure `Sous-titre Funnel`

**Layout :**

```
┌──────┬──────┬──────┬──────┐  ← 4 KPIs
│ Vues │Panier│Achats│Conv. │
└──────┴──────┴──────┴──────┘
┌─────────────────┬──────────┐
│  Funnel d'achat │ Conv.    │
│  (custom)       │ source   │
│                 ├──────────┤
│  + alerte       │ Conv.    │
│  friction       │ device   │
└─────────────────┴──────────┘
┌──────────────────────────────┐
│ Tableau détail conversions   │
└──────────────────────────────┘
```

**4 KPIs :**

| Card | Mesure | Couleur |
|---|---|---|
| Vues totales | `Nb Vues` | `#3B82F6` |
| Ajouts panier | `Nb Ajouts Panier` | `#10B981` |
| Achats | `Nb Achats` | `#10B981` |
| Taux de conversion | `Taux Conversion` | `#F59E0B` |

**Funnel custom :** créer 4 rectangles superposés de largeur décroissante, chacun avec mesure :

| Étape | Largeur relative | Mesure | Couleur |
|---|---|---|---|
| Vues | 100% | `Nb Vues` | `#1E40AF` |
| Ajout panier | ~78% | `Nb Ajouts Panier` | `#10B981` |
| Checkout | ~60% | `Nb Checkout` | `#3B82F6` |
| Achat confirmé | ~48% | `Nb Achats` | `#F59E0B` |

**Encadré "Point de friction" en bas du funnel :** zone de texte avec fond `#3D1F2A`, bordure gauche rouge `#EF4444`, contenant un visuel "Carte" lié à la mesure `Abandon Vues vers Panier`.

**Visuels droite :**

| Visuel | Type | Champs |
|---|---|---|
| Conversion par source | Barre | Axe Y = `fact_web_logs[source]`, Axe X = `[Taux Conversion]` |
| Conversion par device | Barre | Axe Y = `fact_web_logs[device]`, Axe X = `[Taux Conversion]` |
| Tableau détail | Tableau | `source`, `device`, `Nb Vues`, `Nb Ajouts Panier`, `Nb Achats`, `Taux Conversion` |

---

### Page 5 — Satisfaction

**Titre :** `Satisfaction client`
**Sous-titre :** mesure `Sous-titre Satisfaction`

**Layout :**

```
┌──────┬──────┬──────┬──────┐  ← 4 KPIs
│ Note │ Avis │Note<3│% pos.│
└──────┴──────┴──────┴──────┘
┌─────────────────┬──────────┐
│ Distribution    │ Bottom 4 │
│ notes           │ produits │
├─────────────────┼──────────┤
│ Evolution note  │ Tableau  │
│ mensuelle       │ détail   │
└─────────────────┴──────────┘
```

**4 KPIs :**

| Card | Mesure | Couleur |
|---|---|---|
| Note moyenne | `Note Moyenne` | `#3B82F6` |
| Nombre d'avis | `Nb Avis` | `#3B82F6` |
| Produits note <3 | `Nb Produits Note <3` | `#EF4444` |
| % Avis positifs | `Pct Avis Positifs` | `#10B981` |

**Visuels :**

| Visuel | Type | Champs |
|---|---|---|
| Distribution des notes | Barre horizontale | Axe Y = `fact_reviews[rating]` (5,4,3,2,1), Axe X = `[Nb Avis]`, **couleur conditionnelle** : vert si rating ≥ 4, orange si 3, rouge si ≤ 2 |
| Evolution mensuelle | Courbe | Axe X = `Calendrier[Mois_Nom]`, Axe Y = `[Note Moyenne]`, couleur orange `#F59E0B` |
| Bottom 4 produits | Barre (top N=4 ASC) | Axe Y = `dim_products[nom_produit]`, Axe X = `[Note Moyenne Produit]` |
| Tableau détail | Tableau | `nom_produit`, `categorie`, `[Note Moyenne Produit]`, `[Nb Avis]`, `[Tendance Note]` |

---

## Étape 9 — Validation finale

### Checklist Import & modèle

- [ ] 7 fichiers importés sans erreur
- [ ] Auto Date/Time désactivé
- [ ] Table `Calendrier` créée et marquée comme table de dates
- [ ] Colonne calculée `fact_web_logs[session_date]` créée
- [ ] Table `_Mesures` créée (colonne Value masquée)
- [ ] 10 relations actives, aucun chemin ambigu
- [ ] Aucune relation M:M bidirectionnelle

### Checklist Mesures

- [ ] 9 mesures KPIs de base
- [ ] 6 mesures KPIs avancés
- [ ] 6 mesures Variations vs N-1 avec flèches ▲ ▼
- [ ] 6 mesures Couleur Variation (formatage conditionnel)
- [ ] 1 mesure Couleur Segment RFM
- [ ] 10 mesures Funnel digital
- [ ] 4 mesures Segment Produits
- [ ] 6 mesures Sous-titres dynamiques
- [ ] **Total : 48 mesures dans 8 dossiers d'affichage**

### Valeurs attendues sans filtre puis filtre 2024

| Mesure | Sans filtre | Filtre Année=2024 |
|---|---|---|
| `CA Total` | ~21,4 M€ | 3,9 M€ |
| `Marge Totale` | ~9,9 M€ | 1,8 M€ |
| `Taux de Marge` | 46,0% | 46,1% |
| `Nb Commandes` | ~16 026 | 3 018 |
| `Nb Clients` | 3 000 | 3 000 |
| `Panier Moyen` | ~1 337 € | 1 297 € |
| `Note Moyenne` | 3,9 | 3,8 |
| `Quantite Vendue` | ~52 000 | 12 443 |
| `Nb Produits Actifs` | 30 | 30 |
| `Nb Vues` | ~5 448 | 1 059 |
| `Nb Ajouts Panier` | ~1 800 | 320 |
| `Nb Achats` | 456 | 100 |
| `Taux Conversion` | 8,4% | 9,4% |
| `Nb Avis` | ~3 000 | 538 |
| `Pct Avis Positifs` | ~72% | 69% |
| `Variation CA %` | (n/a sans filtre temps) | ▼ -54,3% |
| `Periode Active` | `2022 — 2024` | `janv — dec 2024` |

### Checklist Pages

- [ ] Page 1 Overview : 6 KPI + courbe CA + donut catégories + bar canal + donut paiement
- [ ] Page 2 Produit : 4 KPI + Top 10 + scatter + tableau
- [ ] Page 3 Clients : 3 KPI + 3 charts segments + CA RFM + Top clients
- [ ] Page 4 Funnel : 4 KPI + funnel custom + 2 conversions + tableau
- [ ] Page 5 Satisfaction : 4 KPI + distribution + évolution + Bottom 4 + tableau

### Checklist Navigation & slicers

- [ ] Sidebar visible sur les 5 pages
- [ ] Boutons transparents avec navigation de page
- [ ] Item actif visuellement différencié sur chaque page
- [ ] Slicer Année (boutons) en haut à droite, single select
- [ ] Slicer Trimestre (boutons) en haut à droite, multi-select
- [ ] Synchronisation des slicers sur les 5 pages
- [ ] Sous-titres dynamiques fonctionnels (test en changeant les filtres)

---

## Annexes

### Annexe A — Règles techniques DAX non négociables

- `FILTER(table, [Mesure] = "valeur")` et non `mesure = "valeur"` dans `CALCULATE`
- `VAR ... RETURN` pour toutes les mesures avec logique conditionnelle
- `DIVIDE()` pour toutes les divisions (gestion des zéros)
- `IF(ISBLANK(_result), 0, _result)` sur les mesures de comptage
- `PREVIOUSMONTH(Calendrier[Date])` nécessite la table Calendrier marquée comme table de dates
- `MAX()` ne fonctionne pas sur les booléens : utiliser `SELECTEDVALUE()` ou `FILTER`
- Pour les flèches dans les pastilles : `UNICHAR(9650)` = ▲, `UNICHAR(9660)` = ▼, `UNICHAR(8594)` = →, `UNICHAR(8212)` = —

### Annexe B — Story telling et messages clés

#### Séquence narrative pour le comité de direction

1. **Performance globale** (Overview) → *"CA 3,9M (-54% vs 2023), 3 018 commandes"*
2. **Moteurs de performance** (Produit) → *"iPhone 15 Pro et MacBook Air M3 = 25% du CA, 30 produits actifs"*
3. **Valeur client** (Clients) → *"3 000 clients, 43% Dormants/À réactiver — priorité réactivation"*
4. **Conversion digitale** (Funnel) → *"Conversion 9,4%, mais 69,8% d'abandons Vues→Panier"*
5. **Qualité perçue** (Satisfaction) → *"Note 3,8/5, 4 produits sous 3,5 étoiles à surveiller"*

#### 3 recommandations prioritaires

1. **Stopper l'hémorragie CA (-54,3%)** : investigation urgente sur Ordinateurs + Smartphones
2. **Reconquête clients dormants (43% base)** : campagne email personnalisée Q1
3. **Fix du tunnel d'achat (-69,8% Vues→Panier)** : rework fiche produit + bouton panier

### Annexe C — Fichiers livrables

| Fichier | Localisation | Usage |
|---|---|---|
| `mockup_ecommerce_powerbi.html` | `powerbi/` | Mockup interactif navigateur |
| `mockup_ecommerce_powerbi.pptx` | `powerbi/` | Maquette statique 6 slides éditable |
| `presentation_synthese_ecommerce.pptx` | `powerbi/` | 12 slides synthèse comité de direction |
| `ressources_powerbi.md` | `powerbi/` | Ce document — guide de création |
| `nb4_powerbi.ipynb` | `notebooks/` | Notebook pédagogique original |

### Annexe D — Mapping rapide visuel ↔ mesures

| Visuel dashboard | Mesures utilisées |
|---|---|
| KPI CA card | `CA Total` + `Variation CA %` + `Couleur Variation CA` |
| KPI Marge card | `Marge Totale` + `Variation Marge %` + `Couleur Variation Marge` |
| KPI Commandes card | `Nb Commandes` + `Variation Commandes %` + `Couleur Variation Commandes` |
| KPI Clients card | `Nb Clients` + `Variation Clients %` + `Couleur Variation Clients` |
| KPI Panier card | `Panier Moyen` + `Variation Panier %` + `Couleur Variation Panier` |
| KPI Note card | `Note Moyenne` + `Variation Note` + `Couleur Variation Note` |
| Sous-titre Overview | `Sous-titre Overview` (utilise `Periode Active`) |
| Funnel — étape Vues | `Nb Vues` |
| Funnel — étape Panier | `Nb Ajouts Panier` + `Taux Panier sur Vues` |
| Funnel — étape Checkout | `Nb Checkout` + `Taux Checkout sur Panier` |
| Funnel — étape Achat | `Nb Achats` + `Taux Achat sur Checkout` |
| Funnel — alerte friction | `Abandon Vues vers Panier` |
| Tableau Top 10 produits | `dim_products[nom_produit]` + `[CA Produit]` + `[Marge Produit]` + `[Taux de Marge Produit]` + `[Quantite Vendue]` |
| Donut RFM | `clients_rfm_segments[segment_rfm]` + `[Nb Clients]` + `Couleur Segment RFM` |
| Bottom 4 produits | `dim_products[nom_produit]` + `[Note Moyenne Produit]` |

---

**Fin du document.**
*DataProjectLab — apprendre la data sur des cas concrets, structurés et orientés métier.*
