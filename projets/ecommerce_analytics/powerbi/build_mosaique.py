"""
Genere la mosaique 2x3 du dashboard ShopAfrica+ en PNG haute resolution.

Prerequis :
    pip install pillow

Usage :
    cd D:\\DataProjectLab\\DataProjectLab-projects\\projets\\ecommerce_analytics\\powerbi
    python build_mosaique.py

Sortie :
    images/00_overview_5_pages_mosaic.png  (3840x2160 px)
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import sys

# ============================================================
# Configuration
# ============================================================

ROOT = Path(__file__).parent
SCREENSHOTS_DIR = ROOT / "screenshot"
OUTPUT_DIR = ROOT / "images"
OUTPUT_FILE = OUTPUT_DIR / "00_overview_5_pages_mosaic.png"

# Resolution finale 4K pour rendu net en presentation
CANVAS_W = 3840
CANVAS_H = 2160

# Marges et gouttieres
MARGIN = 48
GAP = 32

# Couleurs DataProjectLab
BG = (15, 31, 58)              # #0F1F3A navy
TILE_BG = (26, 31, 46)         # #1A1F2E
LABEL_BG = (15, 31, 58, 235)   # bandeau label
LABEL_BORDER = (29, 158, 117)  # #1D9E75 vert accent
TEXT_WHITE = (255, 255, 255)
TEXT_GREY = (155, 182, 224)    # #9AB6E0
TEXT_LIGHT = (203, 213, 224)   # #CBD5E0
COVER_BORDER = (74, 95, 136)   # #4A5F88

# Pages dans l'ordre du dashboard
PAGES = [
    ("screenshot 1.png", "1 - OVERVIEW"),
    ("screenshot 2.png", "2 - PRODUITS"),
    ("screenshot 3.png", "3 - CLIENTS"),
    ("screenshot 4.png", "4 - FUNNEL DIGITAL"),
    ("screenshot 5.png", "5 - SATISFACTION"),
]

# ============================================================
# Helpers fontes
# ============================================================

def load_font(size, bold=False):
    """Essaye plusieurs polices systeme Windows."""
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def load_serif(size):
    for path in ["C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/georgia.ttf"]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return load_font(size, bold=True)


# ============================================================
# Construction
# ============================================================

def build_mosaic():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Calcul des dimensions des tuiles
    # 3 colonnes, 2 lignes, marges et gouttieres
    cols, rows = 3, 2
    tile_w = (CANVAS_W - 2 * MARGIN - (cols - 1) * GAP) // cols
    tile_h = (CANVAS_H - 2 * MARGIN - (rows - 1) * GAP) // rows

    print(f"Canvas : {CANVAS_W}x{CANVAS_H}")
    print(f"Tuile  : {tile_w}x{tile_h}")

    # Fond
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), BG)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # ---- Placement des 5 captures ----
    positions = [
        (0, 0), (1, 0), (2, 0),   # ligne 1
        (0, 1), (1, 1),           # ligne 2 (5 captures)
    ]

    for idx, (filename, label) in enumerate(PAGES):
        col, row = positions[idx]
        x = MARGIN + col * (tile_w + GAP)
        y = MARGIN + row * (tile_h + GAP)

        path = SCREENSHOTS_DIR / filename
        if not path.exists():
            print(f"[!] Manquant : {path}")
            continue

        img = Image.open(path).convert("RGB")
        # Resize en preservant le ratio puis crop centre
        ratio_src = img.width / img.height
        ratio_dst = tile_w / tile_h
        if ratio_src > ratio_dst:
            new_h = tile_h
            new_w = int(new_h * ratio_src)
        else:
            new_w = tile_w
            new_h = int(new_w / ratio_src)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        # Crop centre
        left = (new_w - tile_w) // 2
        top = (new_h - tile_h) // 2
        img = img.crop((left, top, left + tile_w, top + tile_h))

        canvas.paste(img, (x, y))

        # Bandeau label en bas a gauche de la tuile
        label_font = load_font(28, bold=True)
        bbox = label_font.getbbox(label)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        pad_x, pad_y = 24, 14
        bw = text_w + 2 * pad_x + 8
        bh = text_h + 2 * pad_y
        bx = x + 24
        by = y + tile_h - bh - 24
        # Fond
        draw.rectangle([bx, by, bx + bw, by + bh], fill=LABEL_BG)
        # Border-left vert accent
        draw.rectangle([bx, by, bx + 6, by + bh], fill=LABEL_BORDER + (255,))
        # Texte
        draw.text((bx + 12 + 8, by + pad_y - bbox[1]), label, font=label_font, fill=TEXT_WHITE)

        print(f"  -> Tuile {idx+1} placee : {label}")

    # ---- 6e tuile : couverture DataProjectLab ----
    col, row = 2, 1
    cx = MARGIN + col * (tile_w + GAP)
    cy = MARGIN + row * (tile_h + GAP)

    # Gradient sombre (simulation par 3 rectangles)
    cover = Image.new("RGB", (tile_w, tile_h), BG)
    cdraw = ImageDraw.Draw(cover)
    # Effet gradient simple : trois bandes
    cdraw.rectangle([0, 0, tile_w, tile_h], fill=(15, 31, 58))
    cdraw.rectangle([0, int(tile_h * 0.4), tile_w, tile_h], fill=(30, 58, 95))
    cdraw.rectangle([0, int(tile_h * 0.7), tile_w, tile_h], fill=(44, 82, 130))
    canvas.paste(cover, (cx, cy))

    # Texte de la couverture
    pad = 56
    # Tag
    tag_font = load_font(22, bold=True)
    draw.text((cx + pad, cy + pad), "DATAPROJECTLAB  -  POWER BI", font=tag_font, fill=TEXT_GREY)

    # Titre Georgia serif
    title_font = load_serif(72)
    draw.text((cx + pad, cy + pad + 56), "ShopAfrica+", font=title_font, fill=TEXT_WHITE)
    draw.text((cx + pad, cy + pad + 56 + 84), "Dashboard 360", font=title_font, fill=TEXT_WHITE)

    # Sous-titre
    sub_font = load_font(28)
    draw.text((cx + pad, cy + pad + 56 + 84 + 100),
              "5 pages  -  72 mesures  -  2 colonnes calculees",
              font=sub_font, fill=TEXT_LIGHT)

    # Separateur
    sep_y = cy + tile_h - pad - 220
    draw.line([(cx + pad, sep_y), (cx + tile_w - pad, sep_y)], fill=COVER_BORDER, width=2)

    # Meta lignes avec puces vertes
    meta_font = load_font(24)
    metas = [
        "Niveau intermediaire",
        "Duree 6 a 8 heures",
        "Power BI Desktop 2.140+",
        "Periode janv - dec 2023",
    ]
    for i, m in enumerate(metas):
        my = sep_y + 30 + i * 42
        # Puce verte
        draw.ellipse([cx + pad, my + 10, cx + pad + 14, my + 24], fill=LABEL_BORDER)
        draw.text((cx + pad + 30, my), m, font=meta_font, fill=TEXT_GREY)

    print(f"  -> Tuile 6 : couverture DataProjectLab")

    # ---- Sauvegarde ----
    canvas.save(OUTPUT_FILE, "PNG", optimize=True)
    print(f"\n[OK] Mosaique sauvee : {OUTPUT_FILE}")
    print(f"     Dimensions : {CANVAS_W}x{CANVAS_H}")


if __name__ == "__main__":
    try:
        build_mosaic()
    except ImportError:
        print("[ERREUR] Pillow n'est pas installe. Lance d'abord :")
        print("    pip install pillow")
        sys.exit(1)
    except Exception as e:
        print(f"[ERREUR] {type(e).__name__} : {e}")
        sys.exit(1)
