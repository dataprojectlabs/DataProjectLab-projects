"""
add_rfm_export_cell.py — Ajoute une cellule SQL d'export de la table `rfm` en CSV
a la fin de la section 6 du notebook corrige Customer Churn.

La nouvelle cellule cree `dataset/clients_rfm.csv` qui sera ensuite charge dans
Power BI comme source supplementaire (table dim de segmentation RFM).

Lance :
    # 1) notebook a cote du script (defaut)
    python add_rfm_export_cell.py

    # 2) notebook ailleurs : passer le chemin en argument
    python add_rfm_export_cell.py "D:\\chemin\\Notebook_1_..._Solution.ipynb"

Le script est idempotent : si la cellule existe deja, il ne fait rien.
"""

import argparse
import json
import sys
from pathlib import Path

DEFAULT_NB_NAME = "Notebook_1_SQL_Analytics_Churn_--_Solution.ipynb"

# Marqueur unique pour reconnaitre la cellule deja ajoutee (idempotence)
EXPORT_MARKER = "COPY rfm TO"

# Cellule d'introduction markdown
INTRO_MD_LINES = [
    "### 6.4 Export de la table RFM pour Power BI\n",
    "\n",
    "#### 🔧 MÉTHODE — pourquoi exporter `rfm` en CSV ?\n",
    "\n",
    "Le guide Power BI charge cette table comme **dimension RFM** dans le modèle (relation 1-1 avec `clients`). Recalculer le RFM directement en DAX serait possible (via `RANKX` + `SUMMARIZE` + `ADDCOLUMNS`), mais c'est lourd pédagogiquement et ralentit l'ouverture du `.pbix`. Mieux : on calcule une fois en SQL, on exporte le résultat, Power BI ne fait que lire.\n",
    "\n",
    "#### 🎯 Objectif\n",
    "\n",
    "Exporter la table `rfm` (créée en section 6.1) au format CSV vers le dossier de sortie défini en Setup (`SAVE_PATH`) — Google Drive sur Colab, `./outputs/` en local. Le fichier sera ensuite déposé dans `dataset/` du projet pour publication GitHub raw et consommation par Power BI."
]

# Cellule de code Python d'export (utilise conn.execute + SAVE_PATH defini en Setup)
EXPORT_SQL_LINES = [
    "# Export de la table rfm vers le dossier SAVE_PATH (defini en Setup)\n",
    "# - Local : ./outputs/clients_rfm.csv\n",
    "# - Colab : /content/drive/MyDrive/DataProjectLab/projects/.../clients_rfm.csv\n",
    "import os\n",
    "\n",
    "out_path = os.path.join(SAVE_PATH, 'clients_rfm.csv')\n",
    "conn.execute(f\"COPY rfm TO '{out_path}' (HEADER, DELIMITER ',');\")\n",
    "\n",
    "# Verification rapide : nombre de lignes ecrites + apercu\n",
    "n = conn.execute('SELECT COUNT(*) FROM rfm').fetchone()[0]\n",
    "print(f'\\u2705 Export termine : {out_path}')\n",
    "print(f'   {n:,} lignes ecrites avec colonnes :')\n",
    "print(f'   id_client, code_offre, ville, statut, jours_depuis_derniere_facture,')\n",
    "print(f'   n_reclamations_6m, arpu_6m, R_score, F_score, M_score')"
]

# Cellule markdown de validation post-export
VALIDATE_MD_LINES = [
    "> ✅ **Vérification** — un fichier `clients_rfm.csv` (~8 000 lignes, 10 colonnes) a été écrit dans `SAVE_PATH`. Il contient pour chaque client : `id_client`, `code_offre`, `ville`, `statut`, `jours_depuis_derniere_facture`, `n_reclamations_6m`, `arpu_6m`, `R_score`, `F_score`, `M_score`. Le segment final (Champions / Loyal / At Risk / Lost / New / Others) sera **recalculé en DAX** dans Power BI à partir des 3 scores.\n",
    "\n",
    "> 📁 **Étape suivante — déposer le CSV dans `dataset/`** : pour que le guide Power BI puisse le charger via GitHub raw, copie le fichier depuis `SAVE_PATH` vers `D:\\DataProjectLab\\DataProjectLab-projects\\projets\\customer_churn_analytics\\dataset\\clients_rfm.csv` puis pousse sur GitHub.\n",
    "\n",
    "> 🏥 **MÉTIER** — En conditions réelles, ce CSV serait un **export hebdomadaire automatisé** (cron + script DuckDB) consommé par le service Power BI via planification de rafraîchissement. C'est ce qui transforme une analyse ponctuelle en **outil de pilotage récurrent**."
]


def make_md_cell(source_lines: list[str]) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source_lines,
    }


def make_code_cell(source_lines: list[str]) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_lines,
    }


def resolve_notebook_path(arg_path: str | None) -> Path:
    if arg_path:
        p = Path(arg_path).expanduser().resolve()
        if not p.exists():
            sys.exit(f"[ERREUR] Fichier introuvable : {p}")
        return p
    p = Path(__file__).with_name(DEFAULT_NB_NAME)
    if p.exists():
        return p
    matches = list(Path.cwd().rglob(DEFAULT_NB_NAME))
    if len(matches) == 1:
        print(f"[INFO] Notebook localise automatiquement : {matches[0]}")
        return matches[0]
    if len(matches) > 1:
        print("[ERREUR] Plusieurs notebooks trouves, precise lequel en argument :")
        for m in matches:
            print(f"  - {m}")
        sys.exit(1)
    sys.exit(
        f"[ERREUR] Notebook introuvable.\n"
        f"  Cherche : {DEFAULT_NB_NAME}\n"
        f"  Lance avec le chemin en argument :\n"
        f"    python add_rfm_export_cell.py \"chemin\\vers\\{DEFAULT_NB_NAME}\""
    )


def cell_already_exists(nb: dict) -> bool:
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            src = cell.get("source", [])
            joined = "".join(src) if isinstance(src, list) else str(src)
            if EXPORT_MARKER in joined:
                return True
    return False


def is_new_pattern(cell_source: str) -> bool:
    """Detecte si la cellule utilise deja le nouveau pattern (conn.execute + SAVE_PATH)."""
    return "conn.execute" in cell_source and "SAVE_PATH" in cell_source


def upgrade_old_export_cell(nb: dict) -> bool:
    """Si une cellule export existe avec l'ancien pattern (%%sql), la remplace par le nouveau.
    Retourne True si une mise a jour a eu lieu.
    """
    cells = nb.get("cells", [])
    for i, cell in enumerate(cells):
        if cell.get("cell_type") != "code":
            continue
        src = cell.get("source", [])
        joined = "".join(src) if isinstance(src, list) else str(src)
        if EXPORT_MARKER in joined and not is_new_pattern(joined):
            # Remplacement de la cellule code
            cells[i] = make_code_cell(EXPORT_SQL_LINES)
            # Verifier si la cellule markdown intro juste avant est presente, sinon ajouter
            # On regarde aussi la cellule markdown de validation juste apres
            return True
    return False


def find_insertion_index(nb: dict) -> int:
    """Cherche la cellule contenant 'Top 50 At Risk les plus prioritaires' (ou
    a defaut le dernier %%sql avant la section 7 'Synthese').
    Retourne l'index APRES lequel inserer.
    """
    cells = nb.get("cells", [])

    # Reperer la cellule SQL du Top 50 At Risk
    last_sql_idx = -1
    synthese_idx = -1
    for i, cell in enumerate(cells):
        src = cell.get("source", [])
        joined = "".join(src) if isinstance(src, list) else str(src)
        if cell.get("cell_type") == "code" and "ORDER BY arpu_6m DESC" in joined:
            last_sql_idx = i
        if cell.get("cell_type") == "markdown" and "## 7. Synthese" in joined.replace("é", "e"):
            synthese_idx = i

    if last_sql_idx >= 0:
        # Inserer apres le dernier SQL du Top 50 + son interpretation
        # Cherche le prochain markdown INTERPRETATION juste apres
        for j in range(last_sql_idx + 1, len(cells)):
            cell = cells[j]
            src = cell.get("source", [])
            joined = "".join(src) if isinstance(src, list) else str(src)
            if cell.get("cell_type") == "markdown" and "INTERPR" in joined:
                return j  # inserer juste apres ce markdown
        return last_sql_idx + 1

    if synthese_idx > 0:
        return synthese_idx  # inserer juste avant section 7

    # Fallback : avant-derniere position (avant footer)
    return max(0, len(cells) - 1)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ajoute la cellule d'export RFM au notebook corrige."
    )
    parser.add_argument("notebook", nargs="?", default=None,
                        help="Chemin vers le notebook (auto-detecte sinon).")
    args = parser.parse_args()

    nb_path = resolve_notebook_path(args.notebook)
    nb = json.loads(nb_path.read_text(encoding="utf-8"))

    if cell_already_exists(nb):
        # Cellule d'export presente : verifier si elle utilise le nouveau pattern
        already_new = any(
            cell.get("cell_type") == "code"
            and is_new_pattern("".join(cell.get("source", [])))
            for cell in nb.get("cells", [])
        )
        if already_new:
            print("[INFO] Cellule deja a jour (pattern conn.execute + SAVE_PATH). Aucun changement.")
            print(f"       Notebook : {nb_path}")
            return 0

        # Sinon : upgrade de l'ancienne cellule vers le nouveau pattern
        if upgrade_old_export_cell(nb):
            nb_path.write_text(
                json.dumps(nb, ensure_ascii=False, indent=1) + "\n",
                encoding="utf-8",
            )
            print("=" * 60)
            print(" Cellule d'export RFM mise a jour")
            print("=" * 60)
            print("  Ancien pattern (%%sql) -> nouveau pattern (conn.execute + SAVE_PATH)")
            print(f"  Notebook reecrit : {nb_path}")
            print("\n  Re-execute la cellule pour generer le CSV dans SAVE_PATH.")
            print("=" * 60)
            return 0

    insertion_idx = find_insertion_index(nb)
    new_cells = [
        make_md_cell(INTRO_MD_LINES),
        make_code_cell(EXPORT_SQL_LINES),
        make_md_cell(VALIDATE_MD_LINES),
    ]

    nb["cells"] = nb["cells"][:insertion_idx + 1] + new_cells + nb["cells"][insertion_idx + 1:]

    nb_path.write_text(
        json.dumps(nb, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )

    print("=" * 60)
    print(" Cellule d'export RFM ajoutee")
    print("=" * 60)
    print(f"  Position d'insertion : apres la cellule {insertion_idx}")
    print(f"  3 nouvelles cellules : 1 markdown intro + 1 code + 1 markdown valid")
    print(f"  Notebook reecrit : {nb_path}")
    print("\n  N'oublie pas de re-executer la cellule pour generer")
    print("  le fichier clients_rfm.csv dans SAVE_PATH !")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
