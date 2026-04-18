# Codes couleurs — EduTrack Analytics
*DataProjectLab · Projet EduTrack · 2024*

---

## Couleurs principales DataProjectLab

| Role | Hex |
|---|---|
| Primary violet | `#534AB7` |
| Violet fonce | `#3C3489` |
| Violet tres fonce (fond couverture) | `#1E1B4B` |
| Violet pale (fond light) | `#EEEDFE` |

---

## Couleurs semantiques

| Role | Hex |
|---|---|
| Vert success | `#1D9E75` |
| Vert fonce | `#0F6E56` |
| Orange warning | `#EF9F27` |
| Orange fonce | `#BA7517` |
| Rouge danger | `#E24B4A` |
| Rouge clair (fond alerte) | `#FCEBEB` |
| Gris neutre | `#888780` |

---

## Fond et cartes

| Role | Hex |
|---|---|
| Fond de page | `#F5F5FA` |
| Cartes blanches | `#FFFFFF` |
| Ombre cartes | `#D4D2EC` |
| Bordure cartes | `#DDDBE8` |
| Fond barres (track vide) | `#EEECF8` |
| Fond alertes rouge clair | `#FAEAEA` |

---

## Textes

| Role | Hex |
|---|---|
| Texte principal | `#3D3A6E` |
| Texte secondaire / labels | `#888780` |
| Texte sidebar inactif | `#9B99C8` |
| Texte sidebar tres discret | `#6B69A8` |

---

## Heatmap — Degradé violet (7 niveaux)

| Intensite | Hex |
|---|---|
| Niveau 1 — tres faible | `#EEEDFE` |
| Niveau 2 | `#D4D1F9` |
| Niveau 3 | `#A89EF0` |
| Niveau 4 | `#7B74E8` |
| Niveau 5 | `#534AB7` |
| Niveau 6 | `#3C3489` |
| Niveau 7 — tres fort | `#1E1B4B` |

---

## Usage semantique — Regle immuable

| Couleur | Signification | Action |
|---|---|---|
| `#E24B4A` Rouge | Alerte critique / Rupture / Danger | Agir aujourd'hui |
| `#EF9F27` Orange | Attention / Warning | Agir cette semaine |
| `#1D9E75` Vert | OK / Succes / Aucun probleme | Aucune action |
| `#534AB7` Violet | Principal DataProjectLab | — |
| `#888780` Gris | Labels / Elements neutres | — |

---

## Parametrage notebooks Python

```python
COLORS = {
    "primary":   "#534AB7",
    "secondary": "#1D9E75",
    "warning":   "#EF9F27",
    "danger":    "#E24B4A",
    "neutral":   "#888780",
    "light":     "#EEEDFE",
}
```

---

## Power BI — Mise en forme conditionnelle

```dax
Couleur Statut =
SWITCH(
    [Statut Stock],
    "RUPTURE IMMINENTE",      "#E24B4A",
    "COMMANDER CETTE SEMAINE","#EF9F27",
    "SURVEILLER",             "#F5D76E",
    "#1D9E75"
)
```
