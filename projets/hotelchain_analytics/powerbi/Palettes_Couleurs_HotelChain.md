# Palettes de couleurs — HotelChain West Analytics
*DataProjectLab · Deux versions de dashboard*

---

## VERSION 1 — Ocean Gradient (Dashboard operationnel)

### Couleurs principales

| Rôle | Nom | Hex | Usage |
|---|---|---|---|
| Primaire | Deep Blue | `#065A82` | Sidebar, header, KPI principal |
| Secondaire | Teal | `#1C7293` | Accent secondaire, barres |
| Fond sombre | Night | `#21295C` | Couverture, fond sidebar |
| Texte principal | Dark | `#1A3A4A` | Corps de texte |

### Couleurs sémantiques

| Rôle | Nom | Hex | Usage |
|---|---|---|---|
| Succès / positif | Emerald | `#1D9E75` | CSAT bon, taux positif |
| Alerte | Amber | `#EF9F27` | Taux annulation, attention |
| Danger | Red | `#E24B4A` | Creux, performances basses |
| Neutre | Slate | `#7A8FA6` | Labels, texte secondaire |

### Fond et cartes

| Rôle | Nom | Hex | Usage |
|---|---|---|---|
| Fond de page | Cream | `#F5F8FA` | Arrière-plan général |
| Cartes | White | `#FFFFFF` | Fond des blocs |
| Bordure | Light Blue | `#D6E4EE` | Bordures cartes |
| Ombre | Shadow | `#C8DCE8` | Ombres portées |

### Heatmap — Dégradé occupation (7 niveaux)

| Intensité | Hex |
|---|---|
| Niveau 1 — très faible | `#CADCFC` |
| Niveau 2 | `#7AADCC` |
| Niveau 3 | `#3A8FA8` |
| Niveau 4 | `#1C7293` |
| Niveau 5 | `#065A82` |
| Niveau 6 | `#1C4A6A` |
| Niveau 7 — très fort | `#21295C` |

---

## VERSION 2 — Dark Luxury (Rapport de direction)

### Couleurs principales

| Rôle | Nom | Hex | Usage |
|---|---|---|---|
| Or primaire | Gold | `#C9A84C` | KPI, accent, lisérés, titres |
| Or clair | Gold Light | `#E8C96A` | Titres Georgia, hover |
| Sable chaud | Sand | `#F0E6D3` | Texte principal sur fond sombre |
| Sable foncé | Sand Dark | `#D4C4A8` | Labels, texte secondaire |

### Fonds

| Rôle | Nom | Hex | Usage |
|---|---|---|---|
| Fond principal | Charcoal | `#1A1A1A` | Fond de page |
| Fond carte | Charcoal 2 | `#232323` | Fond des blocs |
| Fond carte alt. | Charcoal 3 | `#2D2D2D` | Alternance de lignes tableau |
| Élément dim | Dim | `#3A3A3A` | Barres de fond, tracks |

### Couleurs sémantiques

| Rôle | Nom | Hex | Usage |
|---|---|---|---|
| Succès / positif | Emerald | `#4CAF7D` | CSAT bon, performances hautes |
| Alerte | Amber | `#C98A4C` | Attention, second niveau |
| Danger | Bordeaux | `#C94C4C` | Creux, performances basses |
| Neutre | Slate | `#4A5568` | Labels discrets, metadata |

### Heatmap — Dégradé occupation monochrome or (5 niveaux)

| Intensité | Hex |
|---|---|
| Niveau 1 — très faible (fond charbon) | `#1A1A1A` |
| Niveau 2 | `#352C14` |
| Niveau 3 | `#5A4820` |
| Niveau 4 | `#9A7A2E` |
| Niveau 5 — très fort | `#C9A84C` |

---

## Comparaison des deux versions

| Élément | V1 Ocean Gradient | V2 Dark Luxury |
|---|---|---|
| Fond de page | `#F5F8FA` (clair) | `#1A1A1A` (sombre) |
| Couleur dominante | `#065A82` Bleu | `#C9A84C` Or |
| Typographie | Calibri sans-serif | Georgia serif |
| Ambiance | Dashboard opérationnel | Rapport de direction |
| Heatmap | Dégradé bleu | Dégradé or/charbon |
| Cartes | Fond blanc, bordure bleue | Fond charbon, bordure or |

---

## Règle d'usage sémantique (commune aux deux versions)

| Couleur | Signification | Action |
|---|---|---|
| Rouge / Bordeaux | Performance basse / Alerte | Agir immédiatement |
| Orange / Amber | Attention / En dessous de cible | Surveiller |
| Vert / Emerald | Bonne performance | Aucune action |
| Or / Bleu | Neutre / Référence | Indicateur principal |
| Gris / Slate | Metadata, labels | Information secondaire |

---

## Paramétrage Python — V1 Ocean Gradient

```python
COLORS = {
    "primary":   "#065A82",
    "secondary": "#1C7293",
    "success":   "#1D9E75",
    "warning":   "#EF9F27",
    "danger":    "#E24B4A",
    "neutral":   "#7A8FA6",
    "light":     "#F5F8FA",
}
```

## Paramétrage Python — V2 Dark Luxury

```python
COLORS = {
    "primary":   "#C9A84C",
    "secondary": "#4CAF7D",
    "warning":   "#C98A4C",
    "danger":    "#C94C4C",
    "neutral":   "#4A5568",
    "dark":      "#1A1A1A",
    "sand":      "#F0E6D3",
}
```

---

## Power BI — Mise en forme conditionnelle heatmap occupation

```dax
-- V1 Ocean Gradient
Couleur Occupation V1 =
SWITCH(TRUE(),
    [Taux Occupation] >= 0.07, "#21295C",
    [Taux Occupation] >= 0.055,"#065A82",
    [Taux Occupation] >= 0.04, "#1C7293",
    [Taux Occupation] >= 0.03, "#3A8FA8",
    [Taux Occupation] >= 0.02, "#7AADCC",
    "#CADCFC"
)

-- V2 Dark Luxury
Couleur Occupation V2 =
SWITCH(TRUE(),
    [Taux Occupation] >= 0.07, "#C9A84C",
    [Taux Occupation] >= 0.055,"#9A7A2E",
    [Taux Occupation] >= 0.04, "#5A4820",
    [Taux Occupation] >= 0.03, "#352C14",
    "#1A1A1A"
)
```
