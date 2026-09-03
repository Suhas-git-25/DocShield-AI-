"""
DocShield AI - Synthetic Dataset Builder
Generates batches of clean and forged documents across Easy/Medium/Hard tiers,
partitions them into Train (70%), Val (15%), Test (15%) splits with held-out attack types.
"""

import os
import json
import random
from typing import List, Dict, Any, Optional
from PIL import Image

from .generators import generate_id_card, generate_passport, generate_invoice, generate_paystub
from .attacks import ATTACK_DISPATCHER

DOC_GENERATORS = {
    "id_card": generate_id_card,
    "passport": generate_passport,
    "invoice": generate_invoice,
    "paystub": generate_paystub,
}

def generate_dataset_sample(
    doc_id: str,
    doc_type: str = "id_card",
    is_forged: bool = False,
    attack_type: Optional[str] = None,
    severity: str = "medium",
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Generates a single synthetic sample with ground-truth metadata.
    """
    gen_func = DOC_GENERATORS.get(doc_type, generate_id_card)
    img, meta = gen_func(seed=seed)
    meta["doc_id"] = doc_id

    if is_forged:
        if not attack_type:
            attack_type = random.choice(list(ATTACK_DISPATCHER.keys()))
        attack_fn = ATTACK_DISPATCHER.get(attack_type, ATTACK_DISPATCHER["copy_move"])
        img, meta = attack_fn(img, meta, severity=severity)

    return {
        "image": img,
        "metadata": meta
    }

def build_sample_pack(output_dir: str):
    """
    Builds pre-packaged demo documents for instant testing.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    samples_to_build = [
        {"filename": "clean_id_card.png", "type": "id_card", "forged": False, "attack": None, "seed": 101},
        {"filename": "clean_passport.png", "type": "passport", "forged": False, "attack": None, "seed": 102},
        {"filename": "clean_invoice.png", "type": "invoice", "forged": False, "attack": None, "seed": 103},
        {"filename": "clean_paystub.png", "type": "paystub", "forged": False, "attack": None, "seed": 104},
        {"filename": "forged_id_copymove.png", "type": "id_card", "forged": True, "attack": "copy_move", "seed": 201},
        {"filename": "forged_passport_spliced.png", "type": "passport", "forged": True, "attack": "splicing", "seed": 202},
        {"filename": "forged_invoice_fonttamper.png", "type": "invoice", "forged": True, "attack": "font_tamper", "seed": 203},
        {"filename": "forged_paystub_recompressed.png", "type": "paystub", "forged": True, "attack": "recompression", "seed": 204},
        {"filename": "forged_id_geometric.png", "type": "id_card", "forged": True, "attack": "geometric_tamper", "seed": 205},
        {"filename": "forged_invoice_metadata.png", "type": "invoice", "forged": True, "attack": "metadata_tamper", "seed": 206},
    ]

    manifest = []
    for s in samples_to_build:
        res = generate_dataset_sample(
            doc_id=s["filename"].replace(".png", ""),
            doc_type=s["type"],
            is_forged=s["forged"],
            attack_type=s["attack"],
            severity="medium",
            seed=s["seed"]
        )
        img_path = os.path.join(output_dir, s["filename"])
        meta_path = os.path.join(output_dir, s["filename"].replace(".png", ".json"))

        res["image"].save(img_path)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(res["metadata"], f, indent=2)

        manifest.append({
            "filename": s["filename"],
            "document_type": s["type"],
            "is_authentic": not s["forged"],
            "attack_type": s["attack"],
            "anomaly_reason": res["metadata"].get("anomaly_reason"),
            "path": img_path
        })

    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Generated {len(samples_to_build)} demo samples into {output_dir}")

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "sample_data"
    build_sample_pack(out)
