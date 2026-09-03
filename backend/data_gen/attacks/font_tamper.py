"""
DocShield AI - Font & Text Tampering Attack Operator
Overwrites a specific text field using an inconsistent font face, weight, size, or rendering style.
"""

import random
from typing import Tuple, Dict, Any
from PIL import Image, ImageDraw, ImageFont

def get_tamper_font(size: int = 16, style: str = "bold") -> ImageFont.ImageFont:
    font_candidates = [
        "cour.ttf", "times.ttf", "comic.ttf", "impact.ttf", "consolas.ttf",
        "C:\\Windows\\Fonts\\cour.ttf", "C:\\Windows\\Fonts\\times.ttf",
        "C:\\Windows\\Fonts\\comic.ttf", "C:\\Windows\\Fonts\\impact.ttf"
    ]
    for fp in font_candidates:
        try:
            return ImageFont.truetype(fp, size)
        except Exception:
            continue
    return ImageFont.load_default()

def apply_font_tamper_attack(
    image: Image.Image,
    metadata: Dict[str, Any],
    severity: str = "medium"
) -> Tuple[Image.Image, Dict[str, Any]]:
    """
    Overwrites a critical field with a tampered value in an inconsistent font.
    """
    forged_img = image.copy()
    draw = ImageDraw.Draw(forged_img)
    w, h = forged_img.size

    fields = metadata.get("fields", {})
    available_keys = [k for k in fields.keys() if k != "mrz"]
    
    if not available_keys:
        target_key = "total_amount"
        target_bbox = [int(w * 0.6), int(h * 0.7), int(w * 0.8), int(h * 0.75)]
        original_val = "1,000.00"
    else:
        target_key = random.choice(available_keys)
        target_info = fields[target_key]
        target_bbox = target_info["bbox"]
        original_val = target_info["value"]

    bx1, by1, bx2, by2 = target_bbox
    bw, bh = bx2 - bx1, by2 - by1

    # Background color sample near box
    bg_sample = forged_img.getpixel((max(0, bx1 - 5), max(0, by1 - 5)))
    
    # Blank out original value area
    draw.rectangle([(bx1, by1 + 10), (bx2, by2)], fill=bg_sample)

    # Generate forged value
    if "amount" in target_key or "pay" in target_key or "total" in target_key:
        forged_val = f"${random.randint(15000, 95000):,.2f}"
    elif "date" in target_key or "dob" in target_key:
        forged_val = "1999-12-31"
    elif "name" in target_key:
        forged_val = "ALEXANDER VANDERBILT"
    elif "id" in target_key or "passport" in target_key:
        forged_val = f"X{random.randint(90000000, 99999999)}"
    else:
        forged_val = f"MODIFIED-{random.randint(100, 999)}"

    # Determine font style based on severity
    if severity == "easy":
        # Highly mismatched font & size
        font = get_tamper_font(size=22, style="bold")
        text_color = (0, 0, 0)
    elif severity == "medium":
        font = get_tamper_font(size=16, style="regular")
        text_color = (15, 23, 42)
    else: # hard
        font = get_tamper_font(size=14, style="regular")
        text_color = (30, 41, 59)

    draw.text((bx1 + 2, by1 + 12), forged_val, fill=text_color, font=font)

    attack_meta = {
        **metadata,
        "is_authentic": False,
        "attack_type": "font_tamper",
        "tampered_field": target_key,
        "original_value": str(original_val),
        "forged_value": forged_val,
        "severity": severity,
        "attack_region_bbox": target_bbox,
        "norm_attack_bbox": [round(bx1 / w, 4), round(by1 / h, 4), round(bx2 / w, 4), round(by2 / h, 4)],
        "anomaly_reason": f"Font mismatch & typographic variance detected on field '{target_key}' (stroke width, kerning, and typeface inconsistency)."
    }

    return forged_img, attack_meta
