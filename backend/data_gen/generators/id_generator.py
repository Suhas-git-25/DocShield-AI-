"""
DocShield AI - Synthetic ID & Passport Generator
Generates realistic clean identification documents with structured ground-truth fields.
"""

import os
import random
from typing import Tuple, Dict, Any
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from faker import Faker

fake = Faker()

def get_default_font(size: int = 14) -> ImageFont.ImageFont:
    """Attempt to load standard fonts, fallback to default."""
    font_candidates = [
        "arial.ttf",
        "calibri.ttf",
        "segoeui.ttf",
        "DejaVuSans.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibri.ttf",
        "C:\\Windows\\Fonts\\segoeui.ttf",
    ]
    for font_path in font_candidates:
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_guilloche_pattern(draw: ImageDraw.ImageDraw, width: int, height: int, color=(220, 230, 242)):
    """Draw subtle security background curves."""
    for i in range(0, width + height, 25):
        draw.line([(0, i), (i, 0)], fill=color, width=1)
        draw.line([(width, height - i), (width - i, height)], fill=color, width=1)

def generate_id_card(seed: int = None) -> Tuple[Image.Image, Dict[str, Any]]:
    """
    Generates a synthetic National ID Card with ground truth field metadata.
    Returns: (PIL.Image, metadata_dict)
    """
    if seed is not None:
        fake.seed_instance(seed)
        random.seed(seed)

    width, height = 750, 480
    image = Image.new("RGB", (width, height), color=(245, 248, 252))
    draw = ImageDraw.Draw(image)

    # Security background
    draw_guilloche_pattern(draw, width, height, color=(230, 238, 248))

    # Header bar
    header_color = random.choice([(26, 54, 93), (15, 76, 129), (30, 41, 59), (13, 82, 87)])
    draw.rectangle([(0, 0), (width, 70)], fill=header_color)

    font_title = get_default_font(24)
    font_sub = get_default_font(12)
    font_label = get_default_font(12)
    font_val = get_default_font(16)
    font_val_bold = get_default_font(17)

    country = fake.country().upper()
    draw.text((30, 18), f"{country} NATIONAL IDENTITY CARD", fill=(255, 255, 255), font=font_title)
    draw.text((30, 48), "OFFICIAL GOVERNMENT ISSUED IDENTIFICATION", fill=(200, 220, 245), font=font_sub)

    # Gold chip / seal simulation
    draw.rounded_rectangle([(width - 90, 15), (width - 30, 55)], radius=6, fill=(212, 175, 55), outline=(180, 140, 30))
    draw.line([(width - 70, 15), (width - 70, 55)], fill=(180, 140, 30), width=1)
    draw.line([(width - 50, 15), (width - 50, 55)], fill=(180, 140, 30), width=1)

    # Photo Avatar Area
    photo_box = (40, 95, 210, 315)
    draw.rounded_rectangle(photo_box, radius=8, fill=(215, 225, 235), outline=(160, 175, 195), width=2)
    
    # Draw avatar silhouette / features
    avatar_color = (130, 145, 165)
    # Head
    draw.ellipse([(95, 135), (155, 195)], fill=avatar_color)
    # Shoulders
    draw.chord([(65, 205), (185, 330)], start=180, end=360, fill=avatar_color)
    draw.text((75, 285), "PHOTO / PORTRAIT", fill=(100, 115, 135), font=font_sub)

    # Demographic data
    first_name = fake.first_name()
    last_name = fake.last_name().upper()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime("%d %b %Y").upper()
    gender = random.choice(["M", "F"])
    nationality = country[:3].upper()
    id_number = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    issue_date = fake.date_between(start_date="-8y", end_date="-1y").strftime("%d %b %Y").upper()
    expiry_date = fake.date_between(start_date="+2y", end_date="+10y").strftime("%d %b %Y").upper()

    fields_data = [
        {"name": "full_name", "label": "SURNAME / GIVEN NAMES", "value": f"{last_name}, {first_name}", "x": 240, "y": 95, "w": 450, "h": 42},
        {"name": "id_number", "label": "NATIONAL ID NO.", "value": id_number, "x": 240, "y": 145, "w": 240, "h": 42},
        {"name": "dob", "label": "DATE OF BIRTH", "value": dob, "x": 500, "y": 145, "w": 200, "h": 42},
        {"name": "gender", "label": "SEX", "value": gender, "x": 240, "y": 195, "w": 90, "h": 42},
        {"name": "nationality", "label": "NATIONALITY", "value": nationality, "x": 350, "y": 195, "w": 130, "h": 42},
        {"name": "issue_date", "label": "DATE OF ISSUE", "value": issue_date, "x": 500, "y": 195, "w": 200, "h": 42},
        {"name": "expiry_date", "label": "DATE OF EXPIRY", "value": expiry_date, "x": 240, "y": 245, "w": 240, "h": 42},
    ]

    field_metadata = {}
    for f in fields_data:
        # Draw label
        draw.text((f["x"], f["y"]), f["label"], fill=(100, 116, 139), font=font_label)
        # Draw value
        draw.text((f["x"], f["y"] + 16), f["value"], fill=(15, 23, 42), font=font_val_bold)
        
        field_metadata[f["name"]] = {
            "label": f["label"],
            "value": f["value"],
            "bbox": [f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]],
            "norm_bbox": [round(f["x"]/width, 4), round(f["y"]/height, 4), round((f["x"]+f["w"])/width, 4), round((f["y"]+f["h"])/height, 4)]
        }

    # Machine Readable Zone (MRZ) at bottom
    mrz_box = (20, 360, width - 20, 460)
    draw.rectangle(mrz_box, fill=(235, 240, 248), outline=(200, 210, 225))
    font_mrz = get_default_font(18)

    mrz_line1 = f"I<{nationality}{last_name}<<{first_name}<<<<<<<<<<<<<<<<<<<<"[:36]
    clean_id = id_number.replace("-", "")
    mrz_line2 = f"{clean_id}<8{nationality}8501017{gender}2812314<<<<<<<<6"[:36]

    draw.text((40, 375), mrz_line1, fill=(30, 41, 59), font=font_mrz)
    draw.text((40, 415), mrz_line2, fill=(30, 41, 59), font=font_mrz)

    field_metadata["mrz"] = {
        "label": "MRZ CHECKSUM ZONE",
        "value": f"{mrz_line1}\n{mrz_line2}",
        "bbox": [mrz_box[0], mrz_box[1], mrz_box[2], mrz_box[3]],
        "norm_bbox": [round(mrz_box[0]/width, 4), round(mrz_box[1]/height, 4), round(mrz_box[2]/width, 4), round(mrz_box[3]/height, 4)]
    }

    metadata = {
        "document_type": "id_card",
        "width": width,
        "height": height,
        "country": country,
        "fields": field_metadata,
        "photo_box": [photo_box[0], photo_box[1], photo_box[2], photo_box[3]],
        "is_authentic": True,
        "attack_type": None
    }

    return image, metadata


def generate_passport(seed: int = None) -> Tuple[Image.Image, Dict[str, Any]]:
    """
    Generates a synthetic Passport biodata page.
    Returns: (PIL.Image, metadata_dict)
    """
    if seed is not None:
        fake.seed_instance(seed)
        random.seed(seed)

    width, height = 750, 520
    image = Image.new("RGB", (width, height), color=(250, 250, 245))
    draw = ImageDraw.Draw(image)

    # Microprint / watermark lines
    for y in range(80, height - 120, 20):
        draw.line([(20, y), (width - 20, y)], fill=(238, 236, 225), width=1)

    # Header
    country = fake.country().upper()
    font_header = get_default_font(22)
    font_sub = get_default_font(12)
    font_label = get_default_font(11)
    font_val = get_default_font(15)
    font_mrz = get_default_font(17)

    draw.text((40, 20), f"PASSPORT / PASSEPORT — {country}", fill=(30, 41, 59), font=font_header)
    draw.text((40, 48), "TYPE: P   CODE: " + country[:3] + "   PASSPORT NO.", fill=(100, 116, 139), font=font_sub)

    passport_no = f"{random.choice(['A', 'P', 'E'])}{random.randint(10000000, 99999999)}"
    draw.text((260, 48), passport_no, fill=(185, 28, 28), font=font_val)

    # Photo box
    photo_box = (40, 80, 220, 320)
    draw.rectangle(photo_box, fill=(225, 230, 235), outline=(180, 190, 200), width=2)
    avatar_color = (120, 135, 150)
    draw.ellipse([(100, 125), (160, 185)], fill=avatar_color)
    draw.chord([(70, 195), (190, 320)], start=180, end=360, fill=avatar_color)

    # Demographic data
    first_name = fake.first_name()
    last_name = fake.last_name().upper()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=65).strftime("%d/%m/%Y")
    sex = random.choice(["M", "F"])
    place_of_birth = fake.city().upper()
    issue_date = fake.date_between(start_date="-7y", end_date="-1y").strftime("%d/%m/%Y")
    expiry_date = fake.date_between(start_date="+3y", end_date="+10y").strftime("%d/%m/%Y")
    authority = f"{country[:3]} PASSPORT OFFICE"

    fields_data = [
        {"name": "last_name", "label": "SURNAME / NOM", "value": last_name, "x": 250, "y": 80, "w": 450, "h": 36},
        {"name": "first_name", "label": "GIVEN NAMES / PRENOMS", "value": first_name, "x": 250, "y": 120, "w": 450, "h": 36},
        {"name": "nationality", "label": "NATIONALITY / NATIONALITE", "value": country.upper(), "x": 250, "y": 160, "w": 220, "h": 36},
        {"name": "dob", "label": "DATE OF BIRTH / DATE DE NAISSANCE", "value": dob, "x": 480, "y": 160, "w": 220, "h": 36},
        {"name": "sex", "label": "SEX / SEXE", "value": sex, "x": 250, "y": 200, "w": 100, "h": 36},
        {"name": "place_of_birth", "label": "PLACE OF BIRTH / LIEU DE NAISSANCE", "value": place_of_birth, "x": 370, "y": 200, "w": 330, "h": 36},
        {"name": "issue_date", "label": "DATE OF ISSUE / DATE DE DELIVRANCE", "value": issue_date, "x": 250, "y": 240, "w": 220, "h": 36},
        {"name": "expiry_date", "label": "DATE OF EXPIRY / DATE D'EXPIRATION", "value": expiry_date, "x": 480, "y": 240, "w": 220, "h": 36},
        {"name": "authority", "label": "AUTHORITY / AUTORITE", "value": authority, "x": 250, "y": 280, "w": 450, "h": 36},
    ]

    field_metadata = {}
    for f in fields_data:
        draw.text((f["x"], f["y"]), f["label"], fill=(120, 130, 145), font=font_label)
        draw.text((f["x"], f["y"] + 14), f["value"], fill=(15, 23, 42), font=font_val)
        field_metadata[f["name"]] = {
            "label": f["label"],
            "value": f["value"],
            "bbox": [f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]],
            "norm_bbox": [round(f["x"]/width, 4), round(f["y"]/height, 4), round((f["x"]+f["w"])/width, 4), round((f["y"]+f["h"])/height, 4)]
        }

    # Passport MRZ lines
    mrz_y = height - 100
    draw.rectangle([(20, mrz_y - 10), (width - 20, height - 15)], fill=(245, 245, 238), outline=(215, 215, 205))
    
    mrz_l1 = f"P<{country[:3]}{last_name}<<{first_name}<<<<<<<<<<<<<<<<<<<<<<<<<"[:44]
    mrz_l2 = f"{passport_no}<4{country[:3]}9001018{sex}3001012<<<<<<<<<<<<<<06"[:44]

    draw.text((35, mrz_y), mrz_l1, fill=(20, 20, 20), font=font_mrz)
    draw.text((35, mrz_y + 35), mrz_l2, fill=(20, 20, 20), font=font_mrz)

    field_metadata["passport_number"] = {
        "label": "PASSPORT NUMBER",
        "value": passport_no,
        "bbox": [260, 48, 450, 75],
        "norm_bbox": [round(260/width, 4), round(48/height, 4), round(450/width, 4), round(75/height, 4)]
    }

    metadata = {
        "document_type": "passport",
        "width": width,
        "height": height,
        "country": country,
        "fields": field_metadata,
        "photo_box": [photo_box[0], photo_box[1], photo_box[2], photo_box[3]],
        "is_authentic": True,
        "attack_type": None
    }

    return image, metadata
