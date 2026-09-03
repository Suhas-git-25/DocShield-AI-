"""
DocShield AI - Metadata Tampering Attack Operator
Injects or alters EXIF / document metadata tags (e.g., Photoshop signatures, stripped timestamps).
"""

import random
from typing import Tuple, Dict, Any
from PIL import Image

def apply_metadata_tamper_attack(
    image: Image.Image,
    metadata: Dict[str, Any],
    severity: str = "medium"
) -> Tuple[Image.Image, Dict[str, Any]]:
    """
    Simulates metadata alteration and injects editing tool footprints into metadata record.
    """
    forged_img = image.copy()
    w, h = forged_img.size

    editing_tools = [
        "Adobe Photoshop 2024 (Windows)",
        "GIMP 2.10.34",
        "Canva Web Editor",
        "Pixelmator Pro 3.5",
        "PhotoScape X"
    ]
    tamper_software = random.choice(editing_tools)

    attack_meta = {
        **metadata,
        "is_authentic": False,
        "attack_type": "metadata_tamper",
        "severity": severity,
        "tamper_software": tamper_software,
        "exif_flags": {
            "Software": tamper_software,
            "ModifyDate": "2026:08:15 14:22:01",
            "OriginalDate": "2024:02:10 09:15:30",
            "CameraModel": "Scanner / Virtual Device",
            "ColorProfileMismatch": True
        },
        "attack_region_bbox": [0, 0, w, h],
        "norm_attack_bbox": [0.0, 0.0, 1.0, 1.0],
        "anomaly_reason": f"Disallowed editing software signature identified in metadata: '{tamper_software}' with timestamp inconsistency."
    }

    return forged_img, attack_meta
