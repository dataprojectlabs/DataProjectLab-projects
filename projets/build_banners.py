"""
build_banners.py
Genere les banners PNG d'en-tete des notebooks DataProjectLab.

Resolution : 1600x240 px par banner (16:2.4)
Sortie : ../media/banners/banner_<project>.png

Prerequis :
    pip install pillow requests

Usage :
    python build_banners.py                                    # genere les 3 banners
    python build_banners.py --project ecommerce_analytics      # un seul
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import argparse
import sys
import urllib.request

# ============================================================
# Configuration
# ============================================================

ROOT = Path(__file__).parent
LOGO_URL = "https://raw.githubusercontent.com/dataprojectlabs/DataProjectLab-projects/refs/heads/main/media/logo_dataprojectlab.png"
LOGO_CACHE = ROOT / ".cache_logo_dataprojectlab.png"
OUTPUT_DIR = ROOT.parent / "media" / "banners"

# Resolution finale
W = 1600
H = 240

# Couleurs (palette validee DataProjectLab)
GRAD_LEFT = (249, 249, 248)   # #F9F9F8
GRAD_MID = (238, 237, 254)    # #EEEDFE
GRAD_RIGHT = (224, 218, 255)  # #E0DAFF

COLOR_TAG = (83, 74, 183)        # #534AB7 violet primary
COLOR_TITLE = (30, 58, 95)       # #1E3A5F navy
COLOR_SUBTITLE = (83, 74, 183)   # #534AB7
COLOR_META = (107, 114, 128)     # #6B7280 grey
COLOR_BORDER = (199, 210, 254)   # #C7D2FE light violet

# Layout (proportions calees sur le HTML)
PAD_X = 48
PAD_Y = 36
COL_TEXT_W = int(W * 8 / 12)  # 8/12
COL_LOGO_W = W - COL_TEXT_W   # 4/12
LOGO_MAX_W = 280
LOGO_MAX_H = H - PAD_Y * 2

# ============================================================
# Configurations par projet
# ============================================================

PROJECTS = {
    "ecommerce_analytics": {
        "tag": "DATAPROJECTLAB  ·  POWER BI  ·  E-COMMERCE",
        "title": "E-Commerce Analytics 360",
        "subtitle": "Construire le tableau de bord ShopAfrica+ pas a pas",
        "meta": [
            "Niveau Intermediaire",
            "Duree 6 a 8 h",
            "Power BI Desktop 2.140+",
            "5 pages   72 mesures",
        ],
    },
    "customer_support_analytics": {
        "tag": "DATAPROJECTLAB  ·  POWER BI  ·  CUSTOMER SUPPORT",
        "title": "AfriCare Support Analytics",
        "subtitle": "Construire le tableau de bord SLA & Risque ML pas a pas",
        "meta": [
            "Niveau Intermediaire",
            "Duree 6 a 7 h",
            "Power BI Desktop 2.140+",
            "4 pages   48 mesures",
        ],
    },
    "elearning_analytics": {
        "tag": "DATAPROJECTLAB  ·  POWER BI  ·  EDTECH",
        "title": "EduTrack Analytics",
        "subtitle": "Construire le tableau de bord pedagogique pas a pas",
        "meta": [
            "Niveau Intermediaire",
            "Duree 6 a 7 h",
            "Power BI Desktop 2.140+",
            "4 pages",
        ],
    },
}

# ============================================================
# Helpers polices
# ============================================================

def load_font(size, weight="regular"):
    """weight : 'regular' | 'bold' | 'light' | 'semibold'."""
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


# ============================================================
# Helpers gradient et logo
# ============================================================

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

def build_banner(project_id, config):
    print(f"\n[{project_id}]")
    canvas = Image.new("RGB", (W, H), GRAD_LEFT)
    draw_horizontal_gradient(canvas, GRAD_LEFT, GRAD_MID, GRAD_RIGHT)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # ---- COLONNE TEXTE ----
    x = PAD_X
    y = PAD_Y

    # Tag (uppercase, letter-spaced via espaces multiples)
    tag_font = load_font(14, "bold")
    draw.text((x, y), config["tag"], font=tag_font, fill=COLOR_TAG)
    y += 30

    # Titre Georgia serif
    title_font = load_serif(42)
    draw.text((x, y), config["title"], font=title_font, fill=COLOR_TITLE)
    y += 56

    # Sous-titre
    sub_font = load_font(20, "light")
    draw.text((x, y), config["subtitle"], font=sub_font, fill=COLOR_SUBTITLE)
    y += 38

    # Separateur
    sep_y = y + 6
    draw.line(
        [(x, sep_y), (COL_TEXT_W - 16, sep_y)],
        fill=COLOR_BORDER,
        width=1,
    )

    # Meta : items separes par "  -  "
    meta_font = load_font(13, "regular")
    mx = x
    my = sep_y + 12
    for i, item in enumerate(config["meta"]):
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

    # ---- Sauvegarde ----
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / f"banner_{project_id}.png"
    canvas.save(out, "PNG", optimize=True)
    print(f"  -> {out}  ({W}x{H})")


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Genere les banners PNG DataProjectLab.")
    parser.add_argument(
        "--project",
        help=f"ID du projet (defaut : tous). Choix : {', '.join(PROJECTS.keys())}",
    )
    args = parser.parse_args()

    if args.project:
        if args.project not in PROJECTS:
            print(f"[ERREUR] Projet inconnu : {args.project}")
            print(f"Disponibles : {', '.join(PROJECTS.keys())}")
            sys.exit(1)
        build_banner(args.project, PROJECTS[args.project])
    else:
        for pid, cfg in PROJECTS.items():
            build_banner(pid, cfg)

    print("\n[OK] Termine.")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("[ERREUR] Pillow n'est pas installe. Lance : pip install pillow")
        sys.exit(1)
    except Exception as e:
        print(f"[ERREUR] {type(e).__name__} : {e}")
        sys.exit(1)
