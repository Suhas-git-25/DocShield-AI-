"""
DocShield AI - Copy-Move Attack Operator
Clones an existing document patch and pastes it over another target region with edge blending.
"""

import random
from typing import Tuple, Dict, Any, List
from PIL import Image, ImageFilter

def apply_copy_move_attack(
    image: Image.Image,
    metadata: Dict[str, Any],
    severity: str = "medium"
) -> Tuple[Image.Image, Dict[str, Any]]:
    """
    Applies a copy-move forgery attack to an authentic document.
    Severity: 'easy' (harsh edges), 'medium' (subtle blend), 'hard' (micro-aligned)
    """
    forged_img = image.copy()
    w, h = forged_img.size

    fields = metadata.get("fields", {})
    available_keys = [k for k in fields.keys() if k != "mrz"]
    
    if available_keys:
        target_key = random.choice(available_keys)
        target_info = fields[target_key]
        src_bbox = target_info["bbox"]
    else:
        src_bbox = [int(w * 0.3), int(h * 0.3), int(w * 0.5), int(h * 0.4)]

    bx1, by1, bx2, by2 = src_bbox
    bw = max(20, bx2 - bx1)
    bh = max(15, by2 - by1)

    # Crop source region
    patch = forged_img.crop((bx1, by1, bx2, by2))

    # Determine destination location
    offset_x = random.randint(30, min(150, w - bw - 20))
    offset_y = random.randint(-40, 40)
    
    dx1 = max(10, min(w - bw - 10, bx1 + offset_x))
    dy1 = max(10, min(h - bh - 10, by1 + offset_y))
    dx2 = dx1 + bw
    dy2 = dy1 + bh

    # Severity adjustments
    if severity == "easy":
        # Direct paste with hard edges
        forged_img.paste(patch, (dx1, dy1))
    elif severity == "medium":
        # Slight Gaussian blur on borders for blending
        mask = Image.new("L", patch.size, 255)
        mask = mask.filter(ImageFilter.GaussianBlur(1.2))
        forged_img.paste(patch, (dx1, dy1), mask)
    else: # hard
        mask = Image.new("L", patch.size, 255)
        mask = mask.filter(ImageFilter.GaussianBlur(2.5))
        # subtle brightness match
        forged_img.paste(patch, (dx1, dy1), mask)

    attack_meta = {
        **metadata,
        "is_authentic": False,
        "attack_type": "copy_move",
        "severity": severity,
        "attack_region_bbox": [dx1, dy1, dx2, dy2],
        "norm_attack_bbox": [round(dx1 / w, 4), round(dy1 / h, 4), round(dx2 / w, 4), round(dy2 / h, 4)],
        "anomaly_reason": f"Cloned patch detected overlapping region [{dx1}, {dy1}, {dx2}, {dy2}] with identical pixel statistics to source region."
    }

    return forged_img, attack_meta
