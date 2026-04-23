# GoogleAdsPulse — Mesures DAX Power BI

Inventaire complet des mesures DAX présentes dans le **Notebook 3** du projet GoogleAdsPulse.

---

## 📊 Résumé

| Catégorie | Nb mesures |
|---|---|
| **Section 3** — Mesures fondamentales | 10 + 1 bonus |
| **Section 4.1** — Valeurs période précédente | 10 |
| **Section 4.2** — Deltas % | 5 explicites + 5 mentionnés |
| **Section 4.3** — Couleurs conditionnelles | 2 |
| **Section 4.4** — Mesures contextuelles | 10 |
| **Page 4** — Conversions | 4 |
| **TOTAL explicitement écrit en DAX** | **41 mesures** |
| **TOTAL avec les 5 deltas mentionnés "etc."** | **46 mesures** |

Le NB3 annonce "30+ mesures" dans son bilan — ce seuil est largement dépassé.

**Non comptabilisé** : la table calculée `dim_calendrier` (ce n'est pas une mesure mais une table) et les 3 templates génériques (`NomDeLaMesure`, `Mesure Prev`, `Mesure Delta %`) qui servent d'exemples pédagogiques.

---

## Section 3 — Mesures fondamentales (10 + 1)

### Groupe 1 — Volume (3 mesures)

**1. Total Impressions**
```DAX
Total Impressions = SUM(fact_performance[impressions])
```

**2. Total Clicks**
```DAX
Total Clicks = SUM(fact_performance[clicks])
```

**3. Total Conversions**
```DAX
Total Conversions = SUM(fact_performance[conversions])
```

### Groupe 2 — Efficacité (5 mesures)

**4. CTR**
```DAX
CTR = 
DIVIDE(
    [Total Clicks],
    [Total Impressions],
    0
)
```

**5. CPC**
```DAX
CPC = 
DIVIDE(
    SUM(fact_performance[cost_eur]),
    [Total Clicks],
    0
)
```

**6. CPM**
```DAX
CPM = 
DIVIDE(
    SUM(fact_performance[cost_eur]) * 1000,
    [Total Impressions],
    0
)
```

**7. Cost per Conversion**
```DAX
Cost per Conversion = 
DIVIDE(
    SUM(fact_performance[cost_eur]),
    [Total Conversions],
    0
)
```

**8. Conversion Rate**
```DAX
Conversion Rate = 
DIVIDE(
    [Total Conversions],
    [Total Clicks],
    0
)
```

### Groupe 3 — Rentabilité (2 mesures + ROAS bonus)

**9. Total Spend**
```DAX
Total Spend = SUM(fact_performance[cost_eur])
```

**10. Conversions Value**
```DAX
Conversions Value = SUM(fact_performance[conversion_value_eur])
```

**Bonus — ROAS**
```DAX
ROAS = 
DIVIDE(
    [Conversions Value],
    [Total Spend],
    0
)
```

---

## Section 4.1 — Valeurs période précédente (10 mesures)

Toutes ces mesures utilisent `CALCULATE` + `DATEADD` pour décaler le contexte d'un mois en arrière.

**11. Impressions Prev**
```DAX
Impressions Prev = 
CALCULATE([Total Impressions], DATEADD(dim_calendrier[Date], -1, MONTH))
```

**12. Clicks Prev**
```DAX
Clicks Prev = 
CALCULATE([Total Clicks], DATEADD(dim_calendrier[Date], -1, MONTH))
```

**13. Conversions Prev**
```DAX
Conversions Prev = 
CALCULATE([Total Conversions], DATEADD(dim_calendrier[Date], -1, MONTH))
```

**14. CTR Prev**
```DAX
CTR Prev = 
CALCULATE([CTR], DATEADD(dim_calendrier[Date], -1, MONTH))
```

**15. CPC Prev**
```DAX
CPC Prev = 
CALCULATE([CPC], DATEADD(dim_calendrier[Date], -1, MONTH))
```

**16. CPM Prev**
```DAX
CPM Prev = 
CALCULATE([CPM], DATEADD(dim_calendrier[Date], -1, MONTH))
```

**17. Cost per Conversion Prev**
```DAX
Cost per Conversion Prev = 
CALCULATE([Cost per Conversion], DATEADD(dim_calendrier[Date], -1, MONTH))
```

**18. Conversion Rate Prev**
```DAX
Conversion Rate Prev = 
CALCULATE([Conversion Rate], DATEADD(dim_calendrier[Date], -1, MONTH))
```

**19. Total Spend Prev**
```DAX
Total Spend Prev = 
CALCULATE([Total Spend], DATEADD(dim_calendrier[Date], -1, MONTH))
```

**20. Conversions Value Prev**
```DAX
Conversions Value Prev = 
CALCULATE([Conversions Value], DATEADD(dim_calendrier[Date], -1, MONTH))
```

---

## Section 4.2 — Deltas % (5 explicites + 5 mentionnés)

### 5 mesures explicitement écrites

**21. Impressions Delta %**
```DAX
Impressions Delta % = 
DIVIDE([Total Impressions] - [Impressions Prev], [Impressions Prev], 0)
```

**22. Clicks Delta %**
```DAX
Clicks Delta % = 
DIVIDE([Total Clicks] - [Clicks Prev], [Clicks Prev], 0)
```

**23. Conversions Delta %**
```DAX
Conversions Delta % = 
DIVIDE([Total Conversions] - [Conversions Prev], [Conversions Prev], 0)
```

**24. CTR Delta %**
```DAX
CTR Delta % = 
DIVIDE([CTR] - [CTR Prev], [CTR Prev], 0)
```

**25. CPC Delta %**
```DAX
CPC Delta % = 
DIVIDE([CPC] - [CPC Prev], [CPC Prev], 0)
```

### 5 mesures mentionnées "-- etc." (à écrire en suivant le même pattern)

**26. CPM Delta %**
```DAX
CPM Delta % = 
DIVIDE([CPM] - [CPM Prev], [CPM Prev], 0)
```

**27. Cost per Conversion Delta %**
```DAX
Cost per Conversion Delta % = 
DIVIDE([Cost per Conversion] - [Cost per Conversion Prev], [Cost per Conversion Prev], 0)
```

**28. Conversion Rate Delta %**
```DAX
Conversion Rate Delta % = 
DIVIDE([Conversion Rate] - [Conversion Rate Prev], [Conversion Rate Prev], 0)
```

**29. Total Spend Delta %**
```DAX
Total Spend Delta % = 
DIVIDE([Total Spend] - [Total Spend Prev], [Total Spend Prev], 0)
```

**30. Conversions Value Delta %**
```DAX
Conversions Value Delta % = 
DIVIDE([Conversions Value] - [Conversions Value Prev], [Conversions Value Prev], 0)
```

---

## Section 4.3 — Formatage conditionnel couleurs (2 mesures)

**31. Delta Color Good Up** (pour les KPIs où la hausse est bonne)
```DAX
Delta Color Good Up = 
IF([Conversions Delta %] >= 0, "#1D9E75", "#E24B4A")
```

**32. Delta Color Good Down** (pour les KPIs où la baisse est bonne, ex. CPC)
```DAX
Delta Color Good Down = 
IF([CPC Delta %] <= 0, "#1D9E75", "#E24B4A")
```

---

## Section 4.4 — Mesures contextuelles (10 mesures)

**33. ROAS Verdict**
```DAX
ROAS Verdict = 
SWITCH(
    TRUE(),
    [ROAS] >= 5, "⭐ Très rentable",
    [ROAS] >= 3, "✅ Rentable",
    [ROAS] >= 1, "⚠️ Limite",
    "❌ Non rentable"
)
```

**34. Spend 7d MA**
```DAX
Spend 7d MA = 
AVERAGEX(
    DATESINPERIOD(
        dim_calendrier[Date],
        LASTDATE(dim_calendrier[Date]),
        -7,
        DAY
    ),
    [Total Spend]
)
```

**35. Spend YTD**
```DAX
Spend YTD = 
TOTALYTD([Total Spend], dim_calendrier[Date])
```

**36. Nb Campagnes Actives**
```DAX
Nb Campagnes Actives = 
CALCULATE(
    DISTINCTCOUNT(fact_performance[campaign_id]),
    fact_performance[clicks] > 0
)
```

**37. % Spend Account**
```DAX
% Spend Account = 
DIVIDE(
    [Total Spend],
    CALCULATE([Total Spend], ALL(dim_campaigns)),
    0
)
```

**38. Is Anomalie**
```DAX
Is Anomalie = 
IF(
    ISBLANK(RELATED(gads_anomalies[niveau_alerte])),
    "",
    RELATED(gads_anomalies[niveau_alerte])
)
```

**39. QS Moyen**
```DAX
QS Moyen = 
AVERAGE(dim_keywords[quality_score])
```

**40. Purchase Conversions**
```DAX
Purchase Conversions = 
CALCULATE(
    [Total Conversions],
    fact_performance[conversion_type] = "Purchase"
)
```

**41. Lead Conversions**
```DAX
Lead Conversions = 
CALCULATE(
    [Total Conversions],
    fact_performance[conversion_type] IN {"Lead", "Form Submit", "Phone Call"}
)
```

**42. Spend YoY %**
```DAX
Spend YoY % = 
VAR SpendPrevYear = 
    CALCULATE([Total Spend], SAMEPERIODLASTYEAR(dim_calendrier[Date]))
RETURN
    DIVIDE([Total Spend] - SpendPrevYear, SpendPrevYear, 0)
```

---

## Mesures Page 4 — Conversions (4 mesures)

**43. Signup Conversions**
```DAX
Signup Conversions = 
CALCULATE([Total Conversions], fact_performance[conversion_type] = "Signup")
```

**44. Demo Conversions**
```DAX
Demo Conversions = 
CALCULATE([Total Conversions], fact_performance[conversion_type] = "Demo Request")
```

**45. Purchase Value**
```DAX
Purchase Value = 
CALCULATE([Conversions Value], fact_performance[conversion_type] = "Purchase")
```

**46. Cost per Purchase**
```DAX
Cost per Purchase = 
DIVIDE(
    [Total Spend] * DIVIDE([Purchase Conversions], [Total Conversions], 0),
    [Purchase Conversions],
    0
)
```

---

## Table calculée (non comptée comme mesure)

**`dim_calendrier`** — table de dates étendue avec colonnes calculées (Année, Mois, Trimestre, Semaine, Jour, AnneeMois). Indispensable au fonctionnement des mesures temporelles (DATEADD, TOTALYTD, SAMEPERIODLASTYEAR).

```DAX
dim_calendrier = 
ADDCOLUMNS(
    CALENDAR(DATE(2023,1,1), DATE(2024,12,31)),
    "Annee",      YEAR([Date]),
    "Mois_Num",   MONTH([Date]),
    "Mois_Nom",   FORMAT([Date], "MMMM"),
    "Trimestre",  "T" & FORMAT([Date], "Q"),
    "Semaine",    WEEKNUM([Date], 2),
    "Jour_Num",   WEEKDAY([Date], 2),
    "Jour_Nom",   FORMAT([Date], "dddd"),
    "AnneeMois",  FORMAT([Date], "yyyy-MM")
)
```

---

## Templates pédagogiques (non comptés)

Le NB3 contient 3 templates génériques qui servent d'exemples pédagogiques mais ne sont **pas** des mesures à créer :

```DAX
-- Template de base
NomDeLaMesure = EXPRESSION_DAX

-- Pattern général période précédente
Mesure Prev = 
CALCULATE(
    [Mesure Actuelle],
    DATEADD(dim_calendrier[Date], -1, MONTH)
)

-- Pattern général delta %
Mesure Delta % = 
DIVIDE(
    [Mesure Actuelle] - [Mesure Prev],
    [Mesure Prev],
    0
)
```

---

## 📋 Utilisation par page du dashboard

| Page | Mesures utilisées |
|---|---|
| **Page 1 — Overview** | 1 à 10 (KPIs volume/efficacité/rentabilité) + 11 à 30 (deltas) + 31-32 (couleurs) + 34 (Spend 7d MA) + 38 (Is Anomalie) |
| **Page 2 — Campaigns** | 1 à 10 + 33 (ROAS Verdict) + 37 (% Spend Account) + 42 (Spend YoY %) |
| **Page 3 — Keywords** | 2 (Total Clicks) + 4 (CTR) + 39 (QS Moyen) + 36 (Nb Campagnes Actives) |
| **Page 4 — Conversions** | 3 (Total Conversions) + 7 (Cost per Conversion) + 10 (Conversions Value) + 40-41 (Purchase/Lead Conv) + 43-46 (Signup/Demo/Purchase Value/Cost per Purchase) |
| **Page 5 — Breakdown** | 1 à 10 (déclinés par device / country / hour) + 35 (Spend YTD) |

---

**DataProjectLab** — apprendre la data sur des cas concrets, structurés et orientés métier.
