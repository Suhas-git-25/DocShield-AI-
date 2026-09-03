import pytest
from PIL import Image
from backend.data_gen.generators import generate_id_card, generate_invoice
from backend.data_gen.attacks import (
    apply_copy_move_attack,
    apply_splicing_attack,
    apply_font_tamper_attack,
    apply_recompression_attack,
    apply_metadata_tamper_attack,
    apply_geometric_tamper_attack
)

def test_copy_move_attack():
    img, meta = generate_id_card(seed=1)
    forged_img, f_meta = apply_copy_move_attack(img, meta, severity="medium")
    assert isinstance(forged_img, Image.Image)
    assert f_meta["is_authentic"] is False
    assert f_meta["attack_type"] == "copy_move"
    assert len(f_meta["attack_region_bbox"]) == 4

def test_splicing_attack():
    img, meta = generate_id_card(seed=2)
    forged_img, f_meta = apply_splicing_attack(img, meta, severity="easy")
    assert isinstance(forged_img, Image.Image)
    assert f_meta["is_authentic"] is False
    assert f_meta["attack_type"] == "splicing"

def test_font_tamper_attack():
    img, meta = generate_invoice(seed=3)
    forged_img, f_meta = apply_font_tamper_attack(img, meta, severity="medium")
    assert isinstance(forged_img, Image.Image)
    assert f_meta["is_authentic"] is False
    assert f_meta["attack_type"] == "font_tamper"
    assert "tampered_field" in f_meta

def test_recompression_attack():
    img, meta = generate_invoice(seed=4)
    forged_img, f_meta = apply_recompression_attack(img, meta, severity="easy")
    assert isinstance(forged_img, Image.Image)
    assert f_meta["is_authentic"] is False
    assert f_meta["attack_type"] == "recompression"

def test_metadata_tamper_attack():
    img, meta = generate_id_card(seed=5)
    forged_img, f_meta = apply_metadata_tamper_attack(img, meta, severity="medium")
    assert f_meta["is_authentic"] is False
    assert f_meta["attack_type"] == "metadata_tamper"
    assert "exif_flags" in f_meta

def test_geometric_tamper_attack():
    img, meta = generate_id_card(seed=6)
    forged_img, f_meta = apply_geometric_tamper_attack(img, meta, severity="hard")
    assert isinstance(forged_img, Image.Image)
    assert f_meta["is_authentic"] is False
    assert f_meta["attack_type"] == "geometric_tamper"
