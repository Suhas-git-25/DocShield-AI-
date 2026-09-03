"""
DocShield AI - Recompression Artifact Attack Operator
Simulates localized double JPEG recompression (e.g. screenshot-and-edit pattern) generating distinct ELA signatures.
"""

import io
import random
from typing import Tuple, Dict, Any
from PIL import Image

def apply_recompression_attack(
    image: Image.Image,
    metadata: Dict[str, Any],
    severity: str = "medium"
) -> Tuple[Image.Image, Dict[str, Any]]:
    """
    Applies a localized recompression artifact over a target region.
    """
    forged_img = image.copy()
    w, h = forged_img.size

    fields = metadata.get("fields", {})
    available_keys = [k for k in fields.keys() if k != "mrz"]
    
    if available_keys:
        target_key = random.choice(available_keys)
        target_bbox = fields[target_key]["bbox"]
    else:
        target_bbox = [int(w * 0.4), int(h * 0.4), int(w * 0.7), int(h * 0.6)]

    bx1, by1, bx2, by2 = target_bbox
    # Expand box slightly to simulate patch re-saving
    bx1 = max(0, bx1 - 10)
    by1 = max(0, by1 - 10)
    bx2 = min(w, bx2 + 10)
    by2 = min(h, by2 + 10)

    # Crop patch
    patch = forged_img.crop((bx1, by1, bx2, by2))

    # Determine JPEG quality disparity
    if severity == "easy":
        patch_quality = 25
    elif severity == "medium":
        patch_quality = 45
    else: # hard
        patch_quality = 65

    # Recompress patch
    buffer = io.BytesIO()
    patch.save(buffer, format="JPEG", quality=patch_quality)
    buffer.seek(0)
    recompressed_patch = Image.open(buffer).convert("RGB")

    # Paste recompressed patch back
    forged_img.paste(recompressed_patch, (bx1, by1))

    attack_meta = {
        **metadata,
        "is_authentic": False,
        "attack_type": "recompression",
        "patch_quality": patch_quality,
        "severity": severity,
        "attack_region_bbox": [bx1, by1, bx2, by2],
        "norm_attack_bbox": [round(bx1 / w, 4), round(by1 / h, 4), round(bx2 / w, 4), round(by2 / h, 4)],
        "anomaly_reason": f"Localized JPEG recompression artifact detected at [{bx1}, {by1}, {bx2}, {by2}] (Error Level Analysis variance: high DCT grid mismatch)."
    }

    return forged_img, attack_meta
