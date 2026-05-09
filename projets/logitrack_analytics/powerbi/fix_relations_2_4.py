"""
Patch ponctuel pour ressources_powerbi.ipynb — section 2.4 (relations).

1. Remplace le paragraphe approximatif apres la table des relations (qui parlait
   de LOOKUPVALUE de maniere imprecise) par un encadre qui explique pourquoi
   conserver ces 5 relations actives et desactiver les autres.
2. Met a jour le schema ASCII de section 2.1 pour refleter la cle reelle de
   relation transporteurs[nom] -> logitrack_transporteurs_perf[transporteur].

Lance :
    python fix_relations_2_4.py
"""

import json
from pathlib import Path

NB = Path(__file__).with_name("ressources_powerbi.ipynb")

# --- Patch 1 : paragraphe apres la table des relations en 2.4 -----------
OLD_PARA = "Pour les autres outputs (corridors, cout_retard, entrepots_perf), on utilise généralement `LOOKUPVALUE` plutôt qu'une relation, car le grain d'agrégat est différent.\n"

NEW_PARA_LINES = [
    "### ⚠️ Les seules relations actives à conserver\n",
    "\n",
    "Power BI peut détecter automatiquement d'autres relations entre les outputs Python (`logitrack_corridors` ↔ `logitrack_cout_retard` sur `corridor`, `logitrack_corridors` ↔ `logitrack_entrepots_perf` sur `rang_risque`, etc.). **Désactive-les toutes** : ces tables agrégées sont accédées via `LOOKUPVALUE` dans les mesures, jamais par relation. Garder uniquement ces 5 relations évite les filtres croisés indésirables et conserve un schéma en étoile propre.\n",
    "\n",
    "**Comment vérifier** : *Modélisation → Gérer les relations* → seules les 5 lignes ci-dessus doivent être marquées **Active**. Les autres : décocher *Activer cette relation* ou supprimer.\n",
]

# --- Patch 2 : ligne du schema 2.1 corrigee (cle "nom" cote transporteurs) -
OLD_SCHEMA_LINE = "  - logitrack_transporteurs_perf ← rel 1-1 sur transporteur_id\n"
NEW_SCHEMA_LINE = "  - logitrack_transporteurs_perf ← rel 1-1 sur transporteurs[nom] = perf[transporteur]\n"


def patch_block_in_cell(cell, old_line, replacement):
    """Cherche `old_line` (1 ligne exacte) dans cell.source ; si trouvee,
    la remplace par la liste `replacement` (peut etre 1 ou plusieurs lignes).
    Retourne True si modifiee.
    """
    if cell.get("cell_type") != "markdown":
        return False
    src = cell.get("source", [])
    if not isinstance(src, list):
        return False
    for i, line in enumerate(src):
        if line == old_line:
            cell["source"] = src[:i] + list(replacement) + src[i + 1:]
            return True
    return False


def main() -> int:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    n_para = 0
    n_schema = 0

    for cell in nb.get("cells", []):
        if patch_block_in_cell(cell, OLD_PARA, NEW_PARA_LINES):
            n_para += 1
        if patch_block_in_cell(cell, OLD_SCHEMA_LINE, [NEW_SCHEMA_LINE]):
            n_schema += 1

    if n_para == 0 and n_schema == 0:
        print("[INFO] Rien a remplacer (deja corrige ou structure inattendue).")
        return 0

    NB.write_text(
        json.dumps(nb, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    print(f"[OK] Paragraphe 2.4 remplace : {n_para} occurrence(s)")
    print(f"[OK] Ligne 2.1 schema corrigee : {n_schema} occurrence(s)")
    print(f"[OK] Notebook reecrit : {NB}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
