"""
DocShield AI - Splicing Attack Operator
Splices an external entity, altered photo, official seal, or signature into the document.
"""

import random
from typing import Tuple, Dict, Any
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_default_font(size: int = 14) -> ImageFont.ImageFont:
    font_candidates = [
        "arial.ttf", "calibri.ttf", "segoeui.ttf", "DejaVuSans.ttf",
        "C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\calibri.ttf"
    ]
    for fp in font_candidates:
        try:
            return ImageFont.truetype(fp, size)
        except Exception:
            continue
    return ImageFont.load_default()

def create_synthetic_seal(size: int = 100) -> Image.Image:
    """Generates an external foreign government/organization seal."""
    seal = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(seal)
    color = random.choice([(220, 38, 38, 220), (37, 99, 235, 220), (22, 101, 52, 220)])
    
    # Outer ring
    draw.ellipse([(4, 4), (size - 4, size - 4)], outline=color, width=3)
    draw.ellipse([(12, 12), (size - 12, size - 12)], outline=color, width=1)
    
    # Star / Crest inside
    font = get_default_font(10)
    draw.text((size // 4, size // 3), "VERIFIED", fill=color, font=font)
    draw.text((size // 5, size // 2), "* OFFICIAL *", fill=color, font=font)
    return seal

def create_synthetic_photo(width: int = 160, height: int = 210) -> Image.Image:
    """Generates a mismatched foreign portrait photo for splicing."""
    photo = Image.new("RGB", (width, height), color=(random.randint(180, 230), random.randint(180, 230), random.randint(200, 240)))
    draw = ImageDraw.Draw(photo)
    avatar_color = (random.randint(40, 90), random.randint(40, 90), random.randint(70, 110))
    # Head & glasses / silhouette
    draw.ellipse([(width//2 - 30, height//3 - 30), (width//2 + 30, height//3 + 30)], fill=avatar_color)
    draw.chord([(20, height//2), (width - 20, height + 40)], start=180, end=360, fill=avatar_color)
    return photo

def apply_splicing_attack(
    image: Image.Image,
    metadata: Dict[str, Any],
    severity: str = "medium"
) -> Tuple[Image.Image, Dict[str, Any]]:
    """
    Splices a foreign element (photo or seal/stamp) onto the target document.
    """
    forged_img = image.copy().convert("RGBA")
    w, h = forged_img.size
    doc_type = metadata.get("document_type", "id_card")

    if doc_type in ["id_card", "passport"] and "photo_box" in metadata:
        # Splice foreign photo into portrait area
        bx1, by1, bx2, by2 = metadata["photo_box"]
        pw, ph = bx2 - bx1, by2 - by1
        splice_item = create_synthetic_photo(pw, ph).convert("RGBA")
        target_bbox = [bx1, by1, bx2, by2]
        splice_type = "photo_swap"
    else:
        # Splice foreign seal / stamp onto invoice or doc body
        seal_size = random.randint(80, 120)
        splice_item = create_synthetic_seal(seal_size)
        sx1 = random.randint(int(w * 0.4), int(w * 0.75))
        sy1 = random.randint(int(h * 0.4), int(h * 0.75))
        target_bbox = [sx1, sy1, sx1 + seal_size, sy1 + seal_size]
        splice_type = "foreign_seal"

    tx1, ty1, tx2, ty2 = target_bbox
    
    if severity == "easy":
        forged_img.paste(splice_item, (tx1, ty1), splice_item)
    elif severity == "medium":
        # Slight edge blur
        mask = splice_item.split()[3].filter(ImageFilter.GaussianBlur(1.5))
        forged_img.paste(splice_item, (tx1, ty1), mask)
    else: # hard
        mask = splice_item.split()[3].filter(ImageFilter.GaussianBlur(3.0))
        forged_img.paste(splice_item, (tx1, ty1), mask)

    forged_rgb = forged_img.convert("RGB")
    attack_meta = {
        **metadata,
        "is_authentic": False,
        "attack_type": "splicing",
        "splice_subtype": splice_type,
        "severity": severity,
        "attack_region_bbox": target_bbox,
        "norm_attack_bbox": [round(tx1 / w, 4), round(ty1 / h, 4), round(tx2 / w, 4), round(ty2 / h, 4)],
        "anomaly_reason": f"Spliced foreign element ({splice_type}) detected at region [{tx1}, {ty1}, {tx2}, {ty2}] with edge boundary discrepancy."
    }

    return forged_rgb, attack_meta
