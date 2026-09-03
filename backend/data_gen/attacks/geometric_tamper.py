"""
DocShield AI - Geometric Tampering Attack Operator
Applies localized affine shear, perspective distortion, or slight rotation to a subregion.
"""

import random
from typing import Tuple, Dict, Any
from PIL import Image

def apply_geometric_tamper_attack(
    image: Image.Image,
    metadata: Dict[str, Any],
    severity: str = "medium"
) -> Tuple[Image.Image, Dict[str, Any]]:
    """
    Applies a localized geometric warp/rotation over a target region.
    """
    forged_img = image.copy()
    w, h = forged_img.size

    fields = metadata.get("fields", {})
    available_keys = [k for k in fields.keys() if k != "mrz"]
    
    if available_keys:
        target_key = random.choice(available_keys)
        target_bbox = fields[target_key]["bbox"]
    else:
        target_bbox = [int(w * 0.3), int(h * 0.4), int(w * 0.6), int(h * 0.5)]

    bx1, by1, bx2, by2 = target_bbox
    bw, bh = bx2 - bx1, by2 - by1

    patch = forged_img.crop((bx1, by1, bx2, by2))

    if severity == "easy":
        rot_angle = random.choice([-5.0, 5.0])
    elif severity == "medium":
        rot_angle = random.choice([-2.5, 2.5])
    else: # hard
        rot_angle = random.choice([-1.2, 1.2])

    rotated_patch = patch.rotate(rot_angle, resample=Image.BICUBIC, expand=False, fillcolor=(255, 255, 255))
    forged_img.paste(rotated_patch, (bx1, by1))

    attack_meta = {
        **metadata,
        "is_authentic": False,
        "attack_type": "geometric_tamper",
        "severity": severity,
        "rotation_angle": rot_angle,
        "attack_region_bbox": target_bbox,
        "norm_attack_bbox": [round(bx1 / w, 4), round(by1 / h, 4), round(bx2 / w, 4), round(by2 / h, 4)],
        "anomaly_reason": f"Geometric alignment anomaly: Localized perspective angle deviation ({rot_angle}°) detected at region [{bx1}, {by1}, {bx2}, {by2}]."
    }

    return forged_img, attack_meta
