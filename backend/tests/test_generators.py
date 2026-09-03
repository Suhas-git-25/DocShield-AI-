import pytest
from PIL import Image
from backend.data_gen.generators import (
    generate_id_card,
    generate_passport,
    generate_invoice,
    generate_paystub
)

def test_generate_id_card():
    img, meta = generate_id_card(seed=42)
    assert isinstance(img, Image.Image)
    assert img.size == (750, 480)
    assert meta["document_type"] == "id_card"
    assert meta["is_authentic"] is True
    assert "full_name" in meta["fields"]
    assert "id_number" in meta["fields"]
    assert "mrz" in meta["fields"]

def test_generate_passport():
    img, meta = generate_passport(seed=42)
    assert isinstance(img, Image.Image)
    assert meta["document_type"] == "passport"
    assert meta["is_authentic"] is True
    assert "last_name" in meta["fields"]
    assert "passport_number" in meta["fields"]

def test_generate_invoice():
    img, meta = generate_invoice(seed=42)
    assert isinstance(img, Image.Image)
    assert meta["document_type"] == "invoice"
    assert meta["is_authentic"] is True
    assert "vendor_name" in meta["fields"]
    assert "total_amount" in meta["fields"]
    assert meta["grand_total"] > 0

def test_generate_paystub():
    img, meta = generate_paystub(seed=42)
    assert isinstance(img, Image.Image)
    assert meta["document_type"] == "paystub"
    assert meta["is_authentic"] is True
    assert "employer_name" in meta["fields"]
    assert "net_pay" in meta["fields"]
