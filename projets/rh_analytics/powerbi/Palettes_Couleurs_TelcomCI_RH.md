# Palettes de couleurs — TelcomCI RH Analytics
*DataProjectLab · Couleurs officielles DataProjectLab*

---

## COULEURS OFFICIELLES DATAPROJECTLAB

| Rôle | Nom | Hex | Usage |
|---|---|---|---|
| Primaire | Navy DPL | `#1D3461` | Couleur principale de la marque |
| Accent | Orange DPL | `#F47C20` | Accent, CTA, liseré actif |

---

## PALETTE PRINCIPALE — Dashboard TelcomCI RH

### Fonds et structure

| Rôle | Nom | Hex | Usage |
|---|---|---|---|
| Fond sidebar | Charcoal Navy | `#0F1F3D` | Fond de la barre de navigation |
| Fond page | Blue Off-white | `#F0F4FA` | Arrière-plan général des pages |
| Fond carte | White | `#FFFFFF` | Fond des blocs de contenu |
| Fond alterné | Shade | `#E8EEF8` | Lignes alternées des tableaux |
| Bordure carte | Light Blue | `#D6E0F5` | Bordures des cartes arrondies |
| Navy medium | Navy Light | `#2A4A8A` | Badges, barres secondaires |

### Couleurs sémantiques

| Rôle | Nom | Hex | Signification |
|---|---|---|---|
| Positif / Succès | Emerald | `#16A369` | Bonne performance, en dessous du seuil |
| Danger / Alerte | Red | `#E03131` | Turnover élevé, absences critiques |
| Attention | Amber | `#D48A00` | Au-dessus du seuil, à surveiller |
| Orange accent | Orange DPL | `#F47C20` | Variation positive, cible |
| Orange clair | Orange Light | `#F9A05A` | Texte secondaire sur fond sombre |
| Neutre | Slate | `#6B7A99` | Labels, texte secondaire |
| Discret | Muted | `#8898BB` | Texte tertiaire, items inactifs |

---

## APPLICATION PAR COMPOSANT

### Cartes KPI — Liseré coloré

| KPI | Couleur liseré | Hex |
|---|---|---|
| Effectif actif | Navy DPL | `#1D3461` |
| Taux turnover | Red | `#E03131` |
| Note performance | Emerald | `#16A369` |
| Cout turnover | Amber | `#D48A00` |
| Masse salariale | Navy DPL | `#1D3461` |
| Variation mois | Orange DPL | `#F47C20` |
| Absences injustifiées | Red | `#E03131` |
| Hausse absences | Red / Amber | `#E03131` / `#D48A00` |

### Barres horizontales — Sémantique par niveau

| Niveau | Couleur | Hex | Exemple |
|---|---|---|---|
| Critique (> seuil) | Red | `#E03131` | Turnover > 15% |
| Attention (proche seuil) | Amber | `#D48A00` | Turnover 10–15% |
| Normal (< seuil) | Emerald | `#16A369` | Turnover < 10% |
| Référence / total | Navy DPL | `#1D3461` | Masse salariale N°1 |
| Secondaire | Navy Light | `#2A4A8A` | Masse salariale N°2–3 |
| Tertiaire | Slate | `#6B7A99` | Masse salariale N°4–10 |

### Heatmap absentéisme — Dégradé 5 niveaux

| Intensité | Hex | Couleur texte | Seuil |
|---|---|---|---|
| 0 jour | `#F0F4FA` | Navy `#1D3461` | Aucune absence |
| 1–7 jours | `#DDEAF8` | Navy `#1D3461` | Faible |
| 8–14 jours | `#F0B840` | Navy `#1D3461` | Modéré |
| 15–24 jours | `#D48A00` | White `#FFFFFF` | Élevé |
| ≥ 25 jours | `#E03131` | White `#FFFFFF` | Critique |

### Quadrants matrice performance × salaire

| Quadrant | Couleur | Hex | Action |
|---|---|---|---|
| Top Performer Sous-Payé | Red | `#E03131` | Augmentation urgente |
| Top Performer Bien Payé | Emerald | `#16A369` | Fidéliser |
| Faible Perf Bien Payé | Slate | `#6B7A99` | Revoir les missions |
| A Accompagner | Amber | `#D48A00` | Plan de développement |

### Canaux de recrutement

| Rang | Canal | Couleur | Hex |
|---|---|---|---|
| 1–2 (meilleurs) | Cabinet, Référencement | Emerald | `#16A369` |
| 3–4 (moyens) | LinkedIn, Cooptation | Amber | `#D48A00` |
| 5 (le moins bon) | Jobboard | Red | `#E03131` |

---

## PARAMÉTRAGE POWER BI

### Thème JSON — couleurs de base

```json
{
  "name": "TelcomCI RH Analytics",
  "dataColors": [
    "#1D3461",
    "#F47C20",
    "#16A369",
    "#E03131",
    "#D48A00",
    "#2A4A8A",
    "#6B7A99"
  ],
  "background": "#F0F4FA",
  "foreground": "#1D3461",
  "tableAccent": "#F47C20"
}
```

### Mise en forme conditionnelle — Taux turnover

```dax
Couleur Turnover =
SWITCH(TRUE(),
    [Taux Turnover] >= 0.15, "#E03131",   -- Rouge critique
    [Taux Turnover] >= 0.10, "#D48A00",   -- Amber attention
    "#16A369"                              -- Vert normal
)
```

### Mise en forme conditionnelle — Heatmap absences

```dax
Couleur Absences =
SWITCH(TRUE(),
    SUM(vw_absences_valides[nb_jours]) >= 25, "#E03131",
    SUM(vw_absences_valides[nb_jours]) >= 15, "#D48A00",
    SUM(vw_absences_valides[nb_jours]) >= 8,  "#F0B840",
    SUM(vw_absences_valides[nb_jours]) >= 1,  "#DDEAF8",
    "#F0F4FA"
)
```

### Mise en forme conditionnelle — Quadrant performance

```dax
Couleur Quadrant =
VAR _note = [Note Performance Moyenne]
VAR _sal  = [Salaire Net Moyen]
RETURN
SWITCH(
    [Quadrant Performance],
    "Top Performer Sous-Paye",  "#E03131",
    "Top Performer Bien Paye",  "#16A369",
    "Faible Perf Bien Paye",    "#6B7A99",
    "#D48A00"
)
```

---

## PARAMÉTRAGE PYTHON (notebooks)

```python
# Palette TelcomCI RH Analytics — DataProjectLab
COLORS = {
    # Marque
    "navy":       "#1D3461",
    "orange":     "#F47C20",

    # Sémantique
    "success":    "#16A369",
    "danger":     "#E03131",
    "warning":    "#D48A00",
    "neutral":    "#6B7A99",

    # Structure
    "background": "#F0F4FA",
    "card":       "#FFFFFF",
    "shade":      "#E8EEF8",
    "border":     "#D6E0F5",
    "muted":      "#8898BB",
}

# Heatmap absences
HEATMAP_COLORS = {
    0:    "#F0F4FA",   # vide
    1:    "#DDEAF8",   # faible
    8:    "#F0B840",   # modéré
    15:   "#D48A00",   # élevé
    25:   "#E03131",   # critique
}

def heatmap_color(val):
    if val >= 25: return HEATMAP_COLORS[25]
    if val >= 15: return HEATMAP_COLORS[15]
    if val >= 8:  return HEATMAP_COLORS[8]
    if val >= 1:  return HEATMAP_COLORS[1]
    return HEATMAP_COLORS[0]

# Turnover sémantique
def turnover_color(taux_pct):
    if taux_pct >= 15: return COLORS["danger"]
    if taux_pct >= 10: return COLORS["warning"]
    return COLORS["success"]
```

---

## RÉSUMÉ VISUEL — Codes couleurs

```
■ #1D3461  Navy DPL         Primaire marque, fond sidebar
■ #0F1F3D  Charcoal Navy    Fond sidebar profond
■ #2A4A8A  Navy Light       Badges, secondaire
■ #F47C20  Orange DPL       Accent, liseré actif, CTA
■ #F9A05A  Orange Light     Texte secondaire sur fond sombre
■ #16A369  Emerald          Succès, bonne performance
■ #E03131  Red              Danger, alerte critique
■ #D48A00  Amber            Attention, seuil atteint
■ #F0B840  Yellow Amber     Modéré (heatmap niveau 3)
■ #6B7A99  Slate            Labels, neutre
■ #8898BB  Muted            Texte tertiaire, inactif
■ #F0F4FA  Blue Off-white   Fond de page
■ #E8EEF8  Shade            Lignes alternées
■ #D6E0F5  Border Light     Bordures des cartes
■ #FFFFFF  White            Fond carte, texte sur sombre
```
