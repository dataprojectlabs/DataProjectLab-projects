"""
build_banners.py
Genere les banners PNG d'en-tete des notebooks DataProjectLab.

Resolution : 1600x240 px par banner (16:2.4)
Sortie : ../media/banners/banner_<id>.png

Chaque entree de la liste BANNERS produit un PNG.
Pour ajouter un notebook : copier-coller un dict, modifier id/tag/title/subtitle/meta.

Prerequis :
    pip install pillow

Usage :
    python build_banners.py                       # genere TOUS les banners
    python build_banners.py --id ecom_nb1_sol     # un seul (par son id)
    python build_banners.py --filter ecom         # tous ceux dont l'id contient "ecom"
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import argparse
import sys
import urllib.request

# ============================================================
# Liste des banners a generer
# ============================================================
#
# Conventions :
# - id : kebab-case, sert de nom de fichier (banner_<id>.png)
# - tag : ligne du haut en uppercase. Exemples :
#       "DATAPROJECTLAB · VERSION APPRENANT"
#       "DATAPROJECTLAB · VERSION CORRIGEE"
#       "DATAPROJECTLAB · GUIDE POWER BI"
# - title : nom du projet (Georgia bold 42)
# - subtitle : focus du notebook (light 20)
# - meta : 3 a 4 chips affiches en bas
#
# Pour ajouter un notebook : dupliquer un dict et adapter.
# ============================================================

BANNERS = [
    # ---------- E-COMMERCE ANALYTICS ----------
    {
        "id": "ecommerce_main",
        "tag": "DATAPROJECTLAB  ·  POWER BI  ·  E-COMMERCE",
        "title": "E-Commerce Analytics 360",
        "subtitle": "Construire le tableau de bord ShopAfrica+ pas a pas",
        "meta": ["Niveau Intermediaire", "Duree 6 a 8 h", "Python  SQL  Power BI", "5 pages   72 mesures"],
    },
    {
        "id": "ecommerce_nb1_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "E-Commerce Analytics 360",
        "subtitle": "Contexte metier & exploration des donnees",
        "meta": ["Niveau Intermediaire", "Duree 1 a 2 h", "Python  pandas  matplotlib"],
    },
    {
        "id": "ecommerce_nb1_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "E-Commerce Analytics 360",
        "subtitle": "Contexte metier & exploration des donnees",
        "meta": ["Niveau Intermediaire", "Duree 1 a 2 h", "Python  pandas  matplotlib"],
    },
    {
        "id": "ecommerce_nb2_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "E-Commerce Analytics 360",
        "subtitle": "Data cleaning & feature engineering",
        "meta": ["Niveau Intermediaire", "Duree 1 a 2 h", "Python  pandas  numpy"],
    },
    {
        "id": "ecommerce_nb2_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "E-Commerce Analytics 360",
        "subtitle": "Data cleaning & feature engineering",
        "meta": ["Niveau Intermediaire", "Duree 1 a 2 h", "Python  pandas  numpy"],
    },
    {
        "id": "ecommerce_nb3_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "E-Commerce Analytics 360",
        "subtitle": "SQL analytics & segmentation RFM — KPIs e-commerce",
        "meta": ["Niveau Intermediaire", "Duree 2 h", "DuckDB  SQL  CTE  fenetres"],
    },
    {
        "id": "ecommerce_nb3_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "E-Commerce Analytics 360",
        "subtitle": "SQL analytics & segmentation RFM — KPIs e-commerce",
        "meta": ["Niveau Intermediaire", "Duree 2 h", "DuckDB  SQL  CTE  fenetres"],
    },
    {
        "id": "ecommerce_powerbi_guide",
        "tag": "DATAPROJECTLAB  ·  GUIDE POWER BI",
        "title": "E-Commerce Analytics 360",
        "subtitle": "Construire le tableau de bord ShopAfrica+ pas a pas",
        "meta": ["Niveau Intermediaire", "Duree 6 a 8 h", "Power BI Desktop 2.140+", "5 pages   72 mesures"],
    },

    # ---------- CUSTOMER SUPPORT ANALYTICS ----------
    {
        "id": "customer_support_main",
        "tag": "DATAPROJECTLAB  ·  POWER BI  ·  CUSTOMER SUPPORT",
        "title": "AfriCare Support Analytics",
        "subtitle": "Construire le tableau de bord SLA & Risque ML pas a pas",
        "meta": ["Niveau Intermediaire", "Duree 6 a 7 h", "Python  SQL  Power BI", "4 pages   48 mesures"],
    },
    {
        "id": "customer_support_nb1_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "AfriCare Support Analytics",
        "subtitle": "Contexte metier & exploration des tickets",
        "meta": ["Niveau Intermediaire", "Duree 1 a 2 h", "Python  pandas  matplotlib"],
    },
    {
        "id": "customer_support_nb1_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "AfriCare Support Analytics",
        "subtitle": "Contexte metier & exploration des tickets",
        "meta": ["Niveau Intermediaire", "Duree 1 a 2 h", "Python  pandas  matplotlib"],
    },
    {
        "id": "customer_support_nb2_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "AfriCare Support Analytics",
        "subtitle": "SQL analytics — RANK, LAG sur performance agents",
        "meta": ["Niveau Intermediaire", "Duree 2 h", "DuckDB  window functions"],
    },
    {
        "id": "customer_support_nb2_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "AfriCare Support Analytics",
        "subtitle": "SQL analytics — RANK, LAG sur performance agents",
        "meta": ["Niveau Intermediaire", "Duree 2 h", "DuckDB  window functions"],
    },
    {
        "id": "customer_support_nb3_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "AfriCare Support Analytics",
        "subtitle": "Machine learning — 3 modeles & seuil metier",
        "meta": ["Niveau Intermediaire", "Duree 2 h", "scikit-learn  validation temporelle"],
    },
    {
        "id": "customer_support_nb3_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "AfriCare Support Analytics",
        "subtitle": "Machine learning — 3 modeles & seuil metier",
        "meta": ["Niveau Intermediaire", "Duree 2 h", "scikit-learn  validation temporelle"],
    },
    {
        "id": "customer_support_nb4_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "AfriCare Support Analytics",
        "subtitle": "Data Cleaning & Feature Engineering",
        "meta": ["Niveau Intermediaire", "Duree 2 h", " Nettoyage de données · Feature engineering · Logique métier"],
    },
    {
        "id": "customer_support_nb4_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "AfriCare Support Analytics",
        "subtitle": "Data Cleaning & Feature Engineering",
        "meta": ["Niveau Intermediaire", "Duree 3 h", " Nettoyage de données · Feature engineering · Logique métier"],
    },
    {
        "id": "customer_support_powerbi_guide",
        "tag": "DATAPROJECTLAB  ·  GUIDE POWER BI",
        "title": "AfriCare Support Analytics",
        "subtitle": "Construire le tableau de bord SLA & Risque ML pas a pas",
        "meta": ["Niveau Intermediaire", "Duree 6 a 7 h", "Power BI Desktop 2.140+", "4 pages   48 mesures"],
    },

    # ---------- ELEARNING ANALYTICS ----------
    {
        "id": "elearning_main",
        "tag": "DATAPROJECTLAB  ·  POWER BI  ·  EDTECH",
        "title": "EduTrack Analytics",
        "subtitle": "Construire le tableau de bord pedagogique pas a pas",
        "meta": ["Niveau Intermediaire", "Duree 6 a 7 h", "Python  SQL  Power BI"],
    },
    {
        "id": "elearning_nb1_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "EduTrack Analytics",
        "subtitle": "Contexte, Brief Métier & Découverte des Données",
        "meta": ["Niveau Intermediaire", "Duree 2 - 3 h", "Python — pandas, matplotlib"],
    },
    {
        "id": "elearning_nb1_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "EduTrack Analytics",
        "subtitle": "Contexte, Brief Métier & Découverte des Données",
        "meta": ["Niveau Intermediaire", "Duree 3 h", "Python — pandas, matplotlib"],
    },
    {
        "id": "elearning_nb2_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "EduTrack Analytics",
        "subtitle": "Data Cleaning & Feature Engineering",
        "meta": ["Niveau Intermediaire", "Duree 3 h", "Python — pandas, matplotlib"],
    },
    {
        "id": "elearning_nb2_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "EduTrack Analytics",
        "subtitle": "Data Cleaning & Feature Engineering",
        "meta": ["Niveau Intermediaire", "Duree 3 h", "Python — pandas, numpy, matplotlib"],
    },
    {
        "id": "elearning_nb3_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "EduTrack Analytics",
        "subtitle": "SQL Analytics, KPIs & Performance",
        "meta": ["Avancé", "Duree 3 - 4 h", "Python, DuckDB (JupySQL), matplotlib "],
    },
    {
        "id": "elearning_nb3_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "EduTrack Analytics",
        "subtitle": "SQL Analytics, KPIs & Performance",
        "meta": ["Avancé", "Duree 3 - 4 h", "Python, DuckDB (JupySQL), matplotlib "],
    },
    {
        "id": "elearning_nb4_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "EduTrack Analytics",
        "subtitle": "Machine Learning Premium : Détection du Décrochage",
        "meta": ["Avancé", "Duree 3 - 4 h", "scikit-learn — classification, validation temporelle, optimisation seuil"],
    },
    {
        "id": "elearning_nb4_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "EduTrack Analytics",
        "subtitle": "Machine Learning Premium : Détection du Décrochage",
        "meta": ["Avancé", "Duree 3 - 4 h", "scikit-learn — classification, validation temporelle, optimisation seuil"],
    },
    {
        "id": "elearning_powerbi_guide",
        "tag": "DATAPROJECTLAB  ·  GUIDE POWER BI",
        "title": "EduTrack Analytics",
        "subtitle": "Construire le tableau de bord pedagogique pas a pas",
        "meta": ["Niveau Intermediaire", "Duree 6 a 7 h", "Power BI, DAX"],
    },

    # ---------- PHARMACY ANALYTICS (HGU) ----------
    {
        "id": "pharmacy_main",
        "tag": "DATAPROJECTLAB  ·  POWER BI  ·  SANTE",
        "title": "Pharmacy Analytics",
        "subtitle": "Piloter la pharmacie de l'Hopital General Universitaire (HGU)",
        "meta": ["Niveau Intermediaire", "Duree 6 a 8 h", "Python  SQL  Power BI", "4 pages"],
    },
    {
        "id": "pharmacy_nb1_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "Pharmacy Analytics",
        "subtitle": "Contexte, Brief Metier & Decouverte des Donnees",
        "meta": ["Niveau Intermediaire", "Duree 2 - 3 h", "Python — pandas, matplotlib"],
    },
    {
        "id": "pharmacy_nb1_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "Pharmacy Analytics",
        "subtitle": "Contexte, Brief Metier & Decouverte des Donnees",
        "meta": ["Niveau Intermediaire", "Duree 3 h", "Python — pandas, matplotlib"],
    },
    {
        "id": "pharmacy_nb2_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "Pharmacy Analytics",
        "subtitle": "SQL Analytics & EDA — Stocks & Saisonnalite",
        "meta": ["Niveau Intermediaire", "Duree 3 h", "Python, DuckDB (JupySQL), matplotlib"],
    },
    {
        "id": "pharmacy_nb2_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "Pharmacy Analytics",
        "subtitle": "SQL Analytics & EDA — Stocks & Saisonnalite",
        "meta": ["Niveau Intermediaire", "Duree 3 h", "Python, DuckDB (JupySQL), matplotlib"],
    },
    {
        "id": "pharmacy_nb3_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "Pharmacy Analytics",
        "subtitle": "Machine Learning — Prevision de consommation & stock de securite",
        "meta": ["Avance", "Duree 3 - 4 h", "scikit-learn, Prophet, Random Forest"],
    },
    {
        "id": "pharmacy_nb3_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "Pharmacy Analytics",
        "subtitle": "Machine Learning — Prevision de consommation & stock de securite",
        "meta": ["Avance", "Duree 3 - 4 h", "scikit-learn, Prophet, Random Forest"],
    },
    {
        "id": "pharmacy_powerbi_guide",
        "tag": "DATAPROJECTLAB  ·  GUIDE POWER BI",
        "title": "Pharmacy Analytics",
        "subtitle": "Construire le tableau de bord HGU pas a pas",
        "meta": ["Niveau Intermediaire", "Duree 6 a 8 h", "Power BI, DAX", "4 pages"],
    },

    # ---------- HOTELCHAIN ANALYTICS (HotelChainWest) ----------
    {
        "id": "hotelchain_main",
        "tag": "DATAPROJECTLAB  ·  POWER BI  ·  HOSPITALITY",
        "title": "HotelChainWest Analytics",
        "subtitle": "Piloter la performance d'une chaine hoteliere ouest-africaine",
        "meta": ["Niveau Intermediaire", "Duree 6 a 8 h", "Python  SQL  Power BI"],
    },
    {
        "id": "hotelchain_nb1_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "HotelChainWest Analytics",
        "subtitle": "SQL Analytics : KPIs, Performance & Analyses Avancées",
        "meta": ["Niveau Intermediaire", "Duree 4h à 5h ", "Python — pandas, matplotlib"],
    },
    {
        "id": "hotelchain_nb1_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "HotelChainWest Analytics",
        "subtitle": "SQL Analytics : KPIs, Performance & Analyses Avancées",
        "meta": ["Niveau Intermediaire", "Duree 4h à 5h", "Python, DuckDB (JupySQL), pandas matplotlib"],
    },
    {
        "id": "hotelchain_powerbi_guide",
        "tag": "DATAPROJECTLAB  ·  GUIDE POWER BI",
        "title": "HotelChainWest Analytics",
        "subtitle": "Construire le tableau de bord chaine hoteliere pas a pas",
        "meta": ["Niveau Intermediaire", "Duree 6 a 8 h", "Power BI, DAX"],
    },

    # ---------- RH ANALYTICS (TelcomCI) ----------
    {
        "id": "rh_main",
        "tag": "DATAPROJECTLAB  ·  POWER BI  ·  RESSOURCES HUMAINES",
        "title": "TelcomCI RH Analytics",
        "subtitle": "Piloter les RH d'un operateur telecom ivoirien",
        "meta": ["Niveau Intermediaire", "Duree 6 a 8 h", "Python  SQL  Power BI"],
    },
    {
        "id": "rh_nb1_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "TelcomCI RH Analytics",
        "subtitle": "Contexte, Brief Metier & Decouverte des Donnees",
        "meta": ["Niveau Intermediaire", "Duree 2 - 3 h", "Python, matplotlib"],
    },
    {
        "id": "rh_nb1_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "TelcomCI RH Analytics",
        "subtitle": "Contexte, Brief Metier & Decouverte des Donnees",
        "meta": ["Niveau Intermediaire", "Duree 2 - 3 h", "Python, matplotlib"],
    },
    {
        "id": "rh_nb2_enonce",
        "tag": "DATAPROJECTLAB  ·  VERSION APPRENANT",
        "title": "TelcomCI RH Analytics",
        "subtitle": "SQL Analytics : Masse Salariale, Turnover & Performance",
        "meta": ["Niveau Intermediaire", "Duree 3 h", "Python, DuckDB (JupySQL), matplotlib"],
    },
    {
        "id": "rh_nb2_solution",
        "tag": "DATAPROJECTLAB  ·  VERSION CORRIGEE",
        "title": "TelcomCI RH Analytics",
        "subtitle": "SQL Analytics : Masse Salariale, Turnover & Performance",
        "meta": ["Niveau Intermediaire", "Duree 3 h", "Python, DuckDB (JupySQL), matplotlib"],
    },
    {
        "id": "rh_powerbi_guide",
        "tag": "DATAPROJECTLAB  ·  GUIDE POWER BI",
        "title": "TelcomCI RH Analytics",
        "subtitle": "Construire le tableau de bord RH pas a pas",
        "meta": ["Niveau Intermediaire", "Duree 6 a 8 h", "Power BI, DAX"],
    },

]


# ============================================================
# Configuration
# ============================================================

ROOT = Path(__file__).parent
LOGO_URL = "https://raw.githubusercontent.com/dataprojectlabs/DataProjectLab-projects/refs/heads/main/media/logo_dataprojectlab.png"
LOGO_CACHE = ROOT / ".cache_logo_dataprojectlab.png"
OUTPUT_DIR = ROOT.parent / "media" / "banners"

W = 1600
H = 240
BORDER_RADIUS = 32  # rayon des coins arrondis (visible apres scaling notebook)

GRAD_LEFT = (249, 249, 248)
GRAD_MID = (238, 237, 254)
GRAD_RIGHT = (224, 218, 255)

COLOR_TAG = (83, 74, 183)
COLOR_TITLE = (30, 58, 95)
COLOR_SUBTITLE = (83, 74, 183)
COLOR_META = (107, 114, 128)
COLOR_BORDER = (199, 210, 254)

PAD_X = 48
PAD_Y = 36
COL_TEXT_W = int(W * 8 / 12)
COL_LOGO_W = W - COL_TEXT_W
LOGO_MAX_W = 280
LOGO_MAX_H = H - PAD_Y * 2

# ============================================================
# Helpers
# ============================================================

def load_font(size, weight="regular"):
    paths = {
        "regular":  ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"],
        "bold":     ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"],
        "semibold": ["C:/Windows/Fonts/seguisb.ttf", "C:/Windows/Fonts/segoeuib.ttf"],
        "light":    ["C:/Windows/Fonts/segoeuil.ttf", "C:/Windows/Fonts/segoeui.ttf"],
    }
    for p in paths.get(weight, paths["regular"]):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def load_serif(size):
    for p in ["C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/georgia.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return load_font(size, "bold")


def draw_horizontal_gradient(canvas, left_col, mid_col, right_col):
    draw = ImageDraw.Draw(canvas)
    half = W // 2
    for x in range(W):
        if x <= half:
            t = x / half
            r = int(left_col[0] + (mid_col[0] - left_col[0]) * t)
            g = int(left_col[1] + (mid_col[1] - left_col[1]) * t)
            b = int(left_col[2] + (mid_col[2] - left_col[2]) * t)
        else:
            t = (x - half) / (W - half)
            r = int(mid_col[0] + (right_col[0] - mid_col[0]) * t)
            g = int(mid_col[1] + (right_col[1] - mid_col[1]) * t)
            b = int(mid_col[2] + (right_col[2] - mid_col[2]) * t)
        draw.line([(x, 0), (x, H)], fill=(r, g, b))


def download_logo():
    if LOGO_CACHE.exists():
        return LOGO_CACHE
    print("  -> Telechargement du logo DataProjectLab...")
    urllib.request.urlretrieve(LOGO_URL, LOGO_CACHE)
    return LOGO_CACHE


# ============================================================
# Construction d'un banner
# ============================================================

def build_banner(cfg):
    print(f"\n[{cfg['id']}]")
    # On dessine sur un canvas RGB plein, puis on appliquera une mask arrondie
    canvas = Image.new("RGB", (W, H), GRAD_LEFT)
    draw_horizontal_gradient(canvas, GRAD_LEFT, GRAD_MID, GRAD_RIGHT)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # ---- COLONNE TEXTE ----
    x = PAD_X
    y = PAD_Y

    tag_font = load_font(14, "bold")
    draw.text((x, y), cfg["tag"], font=tag_font, fill=COLOR_TAG)
    y += 30

    title_font = load_serif(42)
    draw.text((x, y), cfg["title"], font=title_font, fill=COLOR_TITLE)
    y += 56

    sub_font = load_font(20, "light")
    draw.text((x, y), cfg["subtitle"], font=sub_font, fill=COLOR_SUBTITLE)
    y += 38

    sep_y = y + 6
    draw.line([(x, sep_y), (COL_TEXT_W - 16, sep_y)], fill=COLOR_BORDER, width=1)

    meta_font = load_font(13, "regular")
    mx = x
    my = sep_y + 12
    for i, item in enumerate(cfg["meta"]):
        if i > 0:
            sep = "   -   "
            draw.text((mx, my), sep, font=meta_font, fill=COLOR_BORDER)
            mx += draw.textlength(sep, font=meta_font)
        draw.text((mx, my), item, font=meta_font, fill=COLOR_META)
        mx += draw.textlength(item, font=meta_font)

    # ---- COLONNE LOGO ----
    logo = Image.open(download_logo()).convert("RGBA")
    ratio = min(LOGO_MAX_W / logo.width, LOGO_MAX_H / logo.height)
    new_w = int(logo.width * ratio)
    new_h = int(logo.height * ratio)
    logo = logo.resize((new_w, new_h), Image.LANCZOS)
    logo_x = COL_TEXT_W + (COL_LOGO_W - new_w) // 2
    logo_y = (H - new_h) // 2
    canvas.paste(logo, (logo_x, logo_y), logo)

    # ---- COINS ARRONDIS ----
    # Convertir en RGBA et appliquer une mask de rectangle arrondi
    canvas_rgba = canvas.convert("RGBA")
    mask = Image.new("L", (W, H), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [(0, 0), (W - 1, H - 1)],
        radius=BORDER_RADIUS,
        fill=255,
    )
    rounded = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rounded.paste(canvas_rgba, (0, 0), mask)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / f"banner_{cfg['id']}.png"
    rounded.save(out, "PNG", optimize=True)
    print(f"  -> {out}  ({W}x{H})  border-radius={BORDER_RADIUS}px")


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Genere les banners PNG DataProjectLab.")
    parser.add_argument("--id", help="Genere uniquement le banner avec cet id exact.")
    parser.add_argument("--filter", help="Genere les banners dont l'id contient ce mot.")
    parser.add_argument("--list", action="store_true", help="Liste tous les ids disponibles.")
    args = parser.parse_args()

    if args.list:
        print(f"\n{len(BANNERS)} banners definis :\n")
        for cfg in BANNERS:
            print(f"  {cfg['id']:40s}  {cfg['title']} - {cfg['subtitle']}")
        return

    if args.id:
        match = [c for c in BANNERS if c["id"] == args.id]
        if not match:
            print(f"[ERREUR] Aucun banner avec id='{args.id}'")
            sys.exit(1)
        build_banner(match[0])
    elif args.filter:
        matches = [c for c in BANNERS if args.filter.lower() in c["id"].lower()]
        if not matches:
            print(f"[ERREUR] Aucun banner ne matche le filtre '{args.filter}'")
            sys.exit(1)
        for c in matches:
            build_banner(c)
    else:
        for c in BANNERS:
            build_banner(c)

    print(f"\n[OK] Termine. Banners dans : {OUTPUT_DIR}")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("[ERREUR] Pillow manquant : pip install pillow")
        sys.exit(1)
    except Exception as e:
        print(f"[ERREUR] {type(e).__name__} : {e}")
        sys.exit(1)
