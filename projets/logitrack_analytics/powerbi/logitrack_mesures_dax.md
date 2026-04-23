# LogiTrack — Mesures DAX Power BI

Inventaire complet des mesures DAX présentes dans le **Notebook 4** du projet LogiTrack.

---

## 📊 Résumé

| Groupe | Nb mesures |
|---|---|
| **Groupe 1** — KPIs Globaux | 5 |
| **Groupe 2** — Time Intelligence (évolution) | 3 |
| **Groupe 3** — Alertes ML & Quadrants | 4 |
| **TOTAL** | **12 mesures** |

**Non comptabilisé** : la table calculée `Calendrier` (ce n'est pas une mesure mais une dimension temporelle).

---

## Groupe 1 — KPIs Globaux (5 mesures)

**1. Total Livraisons**
```DAX
Total Livraisons =
COUNTROWS(livraisons)
```

**2. Taux Breach %**
```DAX
Taux Breach % =
DIVIDE(
    CALCULATE(COUNTROWS(livraisons), livraisons[sla_breach] = 1),
    [Total Livraisons]
) * 100
```

**3. CSAT Moyen**
```DAX
CSAT Moyen =
CALCULATE(
    AVERAGEX(
        FILTER(livraisons, NOT ISBLANK(livraisons[csat])
               && livraisons[csat] >= 1 && livraisons[csat] <= 5),
        livraisons[csat]
    )
)
```

**4. Total Pénalités FCFA**
```DAX
Total Pénalités FCFA =
SUM(livraisons[penalite_fcfa])
```

**5. Nb Escalades**
```DAX
Nb Escalades =
CALCULATE(COUNTROWS(livraisons), livraisons[escalade] = 1)
```

---

## Groupe 2 — Time Intelligence (3 mesures)

**6. Taux Breach Mois Précédent %**
```DAX
Taux Breach Mois Précédent % =
CALCULATE(
    [Taux Breach %],
    DATEADD(Calendrier[Date], -1, MONTH)
)
```

**7. Variation Breach %**
```DAX
Variation Breach % =
VAR Current  = [Taux Breach %]
VAR Previous = [Taux Breach Mois Précédent %]
RETURN
IF(NOT ISBLANK(Previous), Current - Previous, BLANK())
```

**8. Taux Breach YTD %**
```DAX
Taux Breach YTD % =
DIVIDE(
    CALCULATE(
        COUNTROWS(livraisons),
        livraisons[sla_breach] = 1,
        DATESYTD(Calendrier[Date])
    ),
    CALCULATE(
        COUNTROWS(livraisons),
        DATESYTD(Calendrier[Date])
    )
) * 100
```

---

## Groupe 3 — Alertes ML & Quadrants (4 mesures)

**9. Nb Alertes Critiques**
```DAX
Nb Alertes Critiques =
CALCULATE(
    COUNTROWS(logitrack_risque_scores),
    logitrack_risque_scores[niveau_urgence] = "Critique"
)
```

**10. Nb Alertes Total**
```DAX
Nb Alertes Total =
CALCULATE(
    COUNTROWS(logitrack_risque_scores),
    logitrack_risque_scores[alerte_retard] = 1
)
```

**11. Bandeau Alerte** (label dynamique pour le bandeau haut de la Page 1)
```DAX
Bandeau Alerte =
VAR NbCrit = [Nb Alertes Critiques]
RETURN
IF(
    NbCrit > 0,
    "⚠️ " & NbCrit & " livraisons en risque critique — intervention requise",
    "✅ Aucune alerte critique en cours"
)
```

**12. Quadrant Transporteur** (classification médiane pour le scatter plot Page 3)
```DAX
Quadrant Transporteur =
VAR BreachMed = CALCULATE(MEDIAN(logitrack_transporteurs_perf[taux_breach_pct]))
VAR CsatMed   = CALCULATE(MEDIAN(logitrack_transporteurs_perf[csat_moyen]))
VAR Breach    = SELECTEDVALUE(logitrack_transporteurs_perf[taux_breach_pct])
VAR Csat      = SELECTEDVALUE(logitrack_transporteurs_perf[csat_moyen])
RETURN
SWITCH(TRUE(),
    Breach <= BreachMed && Csat >= CsatMed, "Top Performer",
    Breach <= BreachMed && Csat <  CsatMed, "Fiable Peu Apprécié",
    Breach >  BreachMed && Csat >= CsatMed, "Apprécié Peu Fiable",
    "À Surveiller"
)
```

---

## Table calculée (non comptée comme mesure)

**`Calendrier`** — table de dates étendue avec colonnes calculées (Année, Mois, Mois Nom, Trimestre, Semaine, Jour Semaine, Weekend, tri mois). Indispensable au fonctionnement des mesures Time Intelligence (DATEADD, DATESYTD).

```DAX
Calendrier =
VAR DateMin = MIN(livraisons[date_creation])
VAR DateMax = MAX(livraisons[date_creation])
RETURN
ADDCOLUMNS(
    CALENDAR(DateMin, DateMax),
    "Année",         YEAR([Date]),
    "Mois",          MONTH([Date]),
    "Mois Nom",      FORMAT([Date], "MMM YYYY"),
    "Mois Nom Court",FORMAT([Date], "MMM"),
    "Trimestre",     "T" & QUARTER([Date]),
    "Semaine",       WEEKNUM([Date]),
    "Jour Semaine",  WEEKDAY([Date], 2),
    "Jour Nom",      FORMAT([Date], "dddd"),
    "Est Weekend",   IF(WEEKDAY([Date], 2) >= 6, 1, 0),
    "Tri Mois",      YEAR([Date]) * 100 + MONTH([Date])
)
```

---

## 📋 Utilisation par page du dashboard

| Page | Titre | Mesures utilisées |
|---|---|---|
| **Page 1** | Vue Executive | 1 · 2 · 3 · 4 · 11 (Bandeau Alerte) |
| **Page 2** | Analyse des Corridors | aucune mesure — visuels basés directement sur `logitrack_corridors.csv` |
| **Page 3** | Performance des Transporteurs | 12 (Quadrant Transporteur) — reste basé sur `logitrack_transporteurs_perf.csv` |
| **Page 4** | CSAT & Qualité de Service | 1 · 2 · 3 · 5 |
| **Page 5** | Alertes ML & Prédictions | 9 · 10 · 11 (Bandeau Alerte) |

---

## 🧭 Points d'architecture à retenir

- La table **`Calendrier`** doit être **marquée comme table de dates** (Power BI Desktop → clic droit → *Marquer comme table de dates*) pour que `DATEADD` et `DATESYTD` fonctionnent.
- Les **Pages 2 et 3** consomment directement les CSV analytiques du NB3 (`logitrack_corridors.csv`, `logitrack_transporteurs_perf.csv`) — pas besoin de mesures DAX supplémentaires, les colonnes pré-calculées suffisent.
- La **Page 5** dépend du NB5 (scores de risque ML) — prévoir un message de substitution si `logitrack_risque_scores` est absent : `IF(ISBLANK([Nb Alertes Total]), "Exécuter le NB5 pour activer les alertes ML", [Nb Alertes Total])`.
- La mesure **`Bandeau Alerte`** est réutilisée sur 2 pages (1 et 5) avec un formatage conditionnel de la couleur de fond (rouge si alertes critiques, vert sinon).

---

**DataProjectLab** — apprendre la data sur des cas concrets, structurés et orientés métier.
