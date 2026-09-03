"""
DocShield AI - Synthetic Invoice & Paystub Generator
Generates realistic clean invoices and paystubs with line items, tax, subtotals, and math consistency.
"""

import random
from typing import Tuple, Dict, Any, List
from PIL import Image, ImageDraw, ImageFont
from faker import Faker

fake = Faker()

def get_default_font(size: int = 14) -> ImageFont.ImageFont:
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

def generate_invoice(seed: int = None) -> Tuple[Image.Image, Dict[str, Any]]:
    """
    Generates a synthetic business invoice with verified totals and line items.
    Returns: (PIL.Image, metadata_dict)
    """
    if seed is not None:
        fake.seed_instance(seed)
        random.seed(seed)

    width, height = 800, 1000
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    font_title = get_default_font(28)
    font_header = get_default_font(18)
    font_bold = get_default_font(14)
    font_regular = get_default_font(13)
    font_small = get_default_font(11)

    # Accent color
    primary_color = random.choice([(37, 99, 235), (15, 118, 110), (79, 70, 229), (30, 41, 59)])
    
    # Header styling
    draw.rectangle([(0, 0), (width, 8)], fill=primary_color)

    company_name = fake.company().upper()
    invoice_no = f"INV-{fake.year()}-{random.randint(1000, 9999)}"
    issue_date = fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d")
    due_date = fake.date_between(start_date="today", end_date="+60d").strftime("%Y-%m-%d")
    
    # Top Section: Vendor details
    draw.text((50, 40), company_name, fill=primary_color, font=font_title)
    draw.text((50, 75), fake.street_address(), fill=(100, 116, 139), font=font_small)
    draw.text((50, 90), f"{fake.city()}, {fake.state_abbr()} {fake.zipcode()}", fill=(100, 116, 139), font=font_small)
    draw.text((50, 105), f"Email: billing@{fake.domain_name()} | Tel: {fake.phone_number()}", fill=(100, 116, 139), font=font_small)

    # Right side: Invoice title & summary
    draw.text((520, 40), "INVOICE", fill=(30, 41, 59), font=font_title)
    draw.text((520, 75), f"Invoice #: {invoice_no}", fill=(30, 41, 59), font=font_bold)
    draw.text((520, 95), f"Issue Date: {issue_date}", fill=(71, 85, 105), font=font_regular)
    draw.text((520, 115), f"Due Date: {due_date}", fill=(71, 85, 105), font=font_regular)

    # Bill To Box
    draw.line([(50, 145), (width - 50, 145)], fill=(226, 232, 240), width=1)
    
    client_name = fake.name()
    client_company = fake.company()
    draw.text((50, 160), "BILLED TO:", fill=(100, 116, 139), font=font_small)
    draw.text((50, 178), client_name, fill=(15, 23, 42), font=font_bold)
    draw.text((50, 196), client_company, fill=(51, 65, 85), font=font_regular)
    draw.text((50, 214), fake.address().replace("\n", ", "), fill=(100, 116, 139), font=font_small)

    # Line Item Table
    table_top = 260
    draw.rectangle([(50, table_top), (width - 50, table_top + 32)], fill=(241, 245, 249))
    draw.text((65, table_top + 8), "DESCRIPTION", fill=(71, 85, 105), font=font_bold)
    draw.text((450, table_top + 8), "QTY", fill=(71, 85, 105), font=font_bold)
    draw.text((540, table_top + 8), "UNIT PRICE", fill=(71, 85, 105), font=font_bold)
    draw.text((670, table_top + 8), "TOTAL", fill=(71, 85, 105), font=font_bold)

    items_list = [
        ("Cloud Infrastructure Architecture & Provisioning", random.randint(1, 3), random.choice([1200.00, 1850.00, 2400.00])),
        ("Security Audit & Vulnerability Assessment", random.randint(1, 2), random.choice([950.00, 1450.00, 2100.00])),
        ("Custom ML Model Fine-Tuning & Evaluation", random.randint(1, 4), random.choice([800.00, 1250.00, 1600.00])),
        ("Database Migration & Schema Optimization", random.randint(1, 2), random.choice([650.00, 1100.00, 1350.00])),
    ]
    
    selected_items = random.sample(items_list, k=random.randint(2, 4))
    
    current_y = table_top + 45
    subtotal = 0.0
    line_item_records = []

    for desc, qty, unit_p in selected_items:
        line_total = round(qty * unit_p, 2)
        subtotal += line_total
        
        draw.text((65, current_y), desc, fill=(30, 41, 59), font=font_regular)
        draw.text((460, current_y), str(qty), fill=(51, 65, 85), font=font_regular)
        draw.text((540, current_y), f"${unit_p:,.2f}", fill=(51, 65, 85), font=font_regular)
        draw.text((670, current_y), f"${line_total:,.2f}", fill=(15, 23, 42), font=font_bold)
        
        draw.line([(50, current_y + 28), (width - 50, current_y + 28)], fill=(241, 245, 249), width=1)
        
        line_item_records.append({
            "description": desc,
            "quantity": qty,
            "unit_price": unit_p,
            "line_total": line_total
        })
        current_y += 36

    tax_rate = 0.0825
    tax_amount = round(subtotal * tax_rate, 2)
    grand_total = round(subtotal + tax_amount, 2)

    # Totals Section
    totals_y = current_y + 30
    draw.text((500, totals_y), "Subtotal:", fill=(100, 116, 139), font=font_regular)
    draw.text((660, totals_y), f"${subtotal:,.2f}", fill=(30, 41, 59), font=font_regular)

    draw.text((500, totals_y + 25), "Tax (8.25%):", fill=(100, 116, 139), font=font_regular)
    draw.text((660, totals_y + 25), f"${tax_amount:,.2f}", fill=(30, 41, 59), font=font_regular)

    # Total Highlight Box
    draw.rectangle([(480, totals_y + 55), (width - 50, totals_y + 98)], fill=(238, 242, 255), outline=primary_color)
    draw.text((500, totals_y + 67), "TOTAL DUE:", fill=primary_color, font=font_bold)
    total_str = f"${grand_total:,.2f}"
    draw.text((640, totals_y + 65), total_str, fill=primary_color, font=font_header)

    # Notes & Payment Details
    notes_y = totals_y + 130
    draw.text((50, notes_y), "PAYMENT INSTRUCTIONS:", fill=(71, 85, 105), font=font_bold)
    draw.text((50, notes_y + 20), f"Bank Name: Global Commerce Bank\nAccount Name: {company_name}\nAccount Number: {fake.bban()[:12]}\nRouting: {random.randint(100000000, 999999999)}", fill=(100, 116, 139), font=font_small)

    field_metadata = {
        "invoice_number": {
            "label": "INVOICE NUMBER",
            "value": invoice_no,
            "bbox": [520, 75, 750, 95],
            "norm_bbox": [round(520/width, 4), round(75/height, 4), round(750/width, 4), round(95/height, 4)]
        },
        "vendor_name": {
            "label": "VENDOR NAME",
            "value": company_name,
            "bbox": [50, 40, 450, 70],
            "norm_bbox": [round(50/width, 4), round(40/height, 4), round(450/width, 4), round(70/height, 4)]
        },
        "client_name": {
            "label": "CLIENT NAME",
            "value": client_name,
            "bbox": [50, 178, 300, 196],
            "norm_bbox": [round(50/width, 4), round(178/height, 4), round(300/width, 4), round(196/height, 4)]
        },
        "issue_date": {
            "label": "ISSUE DATE",
            "value": issue_date,
            "bbox": [520, 95, 750, 115],
            "norm_bbox": [round(520/width, 4), round(95/height, 4), round(750/width, 4), round(115/height, 4)]
        },
        "due_date": {
            "label": "DUE DATE",
            "value": due_date,
            "bbox": [520, 115, 750, 135],
            "norm_bbox": [round(520/width, 4), round(115/height, 4), round(750/width, 4), round(135/height, 4)]
        },
        "subtotal": {
            "label": "SUBTOTAL",
            "value": f"${subtotal:,.2f}",
            "bbox": [660, totals_y, 760, totals_y + 20],
            "norm_bbox": [round(660/width, 4), round(totals_y/height, 4), round(760/width, 4), round((totals_y+20)/height, 4)]
        },
        "tax_amount": {
            "label": "TAX AMOUNT",
            "value": f"${tax_amount:,.2f}",
            "bbox": [660, totals_y + 25, 760, totals_y + 45],
            "norm_bbox": [round(660/width, 4), round((totals_y+25)/height, 4), round(760/width, 4), round((totals_y+45)/height, 4)]
        },
        "total_amount": {
            "label": "TOTAL AMOUNT",
            "value": total_str,
            "bbox": [640, totals_y + 55, 770, totals_y + 98],
            "norm_bbox": [round(640/width, 4), round((totals_y+55)/height, 4), round(770/width, 4), round((totals_y+98)/height, 4)]
        }
    }

    metadata = {
        "document_type": "invoice",
        "width": width,
        "height": height,
        "vendor": company_name,
        "client": client_name,
        "items": line_item_records,
        "subtotal": subtotal,
        "tax_amount": tax_amount,
        "grand_total": grand_total,
        "fields": field_metadata,
        "is_authentic": True,
        "attack_type": None
    }

    return image, metadata


def generate_paystub(seed: int = None) -> Tuple[Image.Image, Dict[str, Any]]:
    """
    Generates a synthetic Earnings Statement / Paystub.
    Returns: (PIL.Image, metadata_dict)
    """
    if seed is not None:
        fake.seed_instance(seed)
        random.seed(seed)

    width, height = 800, 950
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    font_title = get_default_font(24)
    font_bold = get_default_font(13)
    font_regular = get_default_font(12)
    font_small = get_default_font(10)

    # Employer & Header
    employer_name = fake.company().upper()
    employee_name = fake.name()
    employee_id = f"EMP-{random.randint(10000, 99999)}"
    pay_period_start = fake.date_between(start_date="-30d", end_date="-15d").strftime("%m/%d/%Y")
    pay_period_end = fake.date_between(start_date="-14d", end_date="today").strftime("%m/%d/%Y")
    pay_date = pay_period_end

    draw.rectangle([(40, 30), (width - 40, 90)], fill=(248, 250, 252), outline=(203, 213, 225))
    draw.text((55, 42), employer_name, fill=(15, 23, 42), font=font_title)
    draw.text((55, 70), "EARNINGS STATEMENT / PAY STUB", fill=(100, 116, 139), font=font_small)

    draw.text((520, 45), f"Pay Date: {pay_date}", fill=(30, 41, 59), font=font_bold)
    draw.text((520, 65), f"Period: {pay_period_start} - {pay_period_end}", fill=(71, 85, 105), font=font_regular)

    # Employee Details Box
    draw.rectangle([(40, 105), (width - 40, 175)], fill=(255, 255, 255), outline=(226, 232, 240))
    draw.text((55, 115), "EMPLOYEE NAME:", fill=(100, 116, 139), font=font_small)
    draw.text((55, 130), employee_name, fill=(15, 23, 42), font=font_bold)
    draw.text((55, 150), f"ID: {employee_id}  |  SSN: ***-**-{random.randint(1000, 9999)}", fill=(71, 85, 105), font=font_small)

    draw.text((450, 115), "DEPARTMENT / ROLE:", fill=(100, 116, 139), font=font_small)
    draw.text((450, 130), fake.job(), fill=(15, 23, 42), font=font_regular)

    # Earnings & Deductions Tables
    table_y = 195
    col_w = (width - 90) // 2
    
    # Left: Earnings
    draw.rectangle([(40, table_y), (40 + col_w, table_y + 24)], fill=(241, 245, 249))
    draw.text((50, table_y + 5), "EARNINGS", fill=(30, 41, 59), font=font_bold)
    draw.text((220, table_y + 5), "HOURS", fill=(30, 41, 59), font=font_bold)
    draw.text((310, table_y + 5), "AMOUNT", fill=(30, 41, 59), font=font_bold)

    hourly_rate = random.choice([45.0, 55.0, 68.0, 82.0, 95.0])
    reg_hours = 80.0
    reg_pay = round(reg_hours * hourly_rate, 2)
    bonus = random.choice([0.0, 500.0, 1000.0])
    gross_pay = round(reg_pay + bonus, 2)

    draw.text((50, table_y + 35), "Regular Pay", fill=(51, 65, 85), font=font_regular)
    draw.text((230, table_y + 35), f"{reg_hours:.1f}", fill=(51, 65, 85), font=font_regular)
    draw.text((310, table_y + 35), f"${reg_pay:,.2f}", fill=(15, 23, 42), font=font_regular)

    if bonus > 0:
        draw.text((50, table_y + 60), "Performance Bonus", fill=(51, 65, 85), font=font_regular)
        draw.text((310, table_y + 60), f"${bonus:,.2f}", fill=(15, 23, 42), font=font_regular)

    # Right: Deductions
    r_x = 40 + col_w + 10
    draw.rectangle([(r_x, table_y), (width - 40, table_y + 24)], fill=(241, 245, 249))
    draw.text((r_x + 10, table_y + 5), "TAXES & DEDUCTIONS", fill=(30, 41, 59), font=font_bold)
    draw.text((width - 130, table_y + 5), "AMOUNT", fill=(30, 41, 59), font=font_bold)

    fed_tax = round(gross_pay * 0.15, 2)
    state_tax = round(gross_pay * 0.05, 2)
    soc_sec = round(gross_pay * 0.062, 2)
    medicare = round(gross_pay * 0.0145, 2)
    total_deductions = round(fed_tax + state_tax + soc_sec + medicare, 2)
    net_pay = round(gross_pay - total_deductions, 2)

    deducts = [
        ("Federal Income Tax", fed_tax),
        ("State Income Tax", state_tax),
        ("Social Security", soc_sec),
        ("Medicare", medicare),
    ]

    for idx, (d_name, d_amt) in enumerate(deducts):
        curr_dy = table_y + 35 + (idx * 25)
        draw.text((r_x + 10, curr_dy), d_name, fill=(51, 65, 85), font=font_regular)
        draw.text((width - 130, curr_dy), f"${d_amt:,.2f}", fill=(15, 23, 42), font=font_regular)

    # Summary Box
    sum_y = table_y + 170
    draw.rectangle([(40, sum_y), (width - 40, sum_y + 70)], fill=(248, 250, 252), outline=(203, 213, 225))
    draw.text((60, sum_y + 15), "GROSS PAY", fill=(100, 116, 139), font=font_small)
    draw.text((60, sum_y + 35), f"${gross_pay:,.2f}", fill=(30, 41, 59), font=font_bold)

    draw.text((280, sum_y + 15), "TOTAL DEDUCTIONS", fill=(100, 116, 139), font=font_small)
    draw.text((280, sum_y + 35), f"-${total_deductions:,.2f}", fill=(185, 28, 28), font=font_bold)

    draw.text((540, sum_y + 15), "NET PAY (TAKE HOME)", fill=(13, 148, 136), font=font_small)
    net_pay_str = f"${net_pay:,.2f}"
    draw.text((540, sum_y + 32), net_pay_str, fill=(13, 148, 136), font=font_title)

    field_metadata = {
        "employer_name": {
            "label": "EMPLOYER NAME",
            "value": employer_name,
            "bbox": [55, 42, 450, 70],
            "norm_bbox": [round(55/width, 4), round(42/height, 4), round(450/width, 4), round(70/height, 4)]
        },
        "employee_name": {
            "label": "EMPLOYEE NAME",
            "value": employee_name,
            "bbox": [55, 130, 350, 150],
            "norm_bbox": [round(55/width, 4), round(130/height, 4), round(350/width, 4), round(150/height, 4)]
        },
        "pay_date": {
            "label": "PAY DATE",
            "value": pay_date,
            "bbox": [520, 45, 750, 65],
            "norm_bbox": [round(520/width, 4), round(45/height, 4), round(750/width, 4), round(65/height, 4)]
        },
        "gross_pay": {
            "label": "GROSS PAY",
            "value": f"${gross_pay:,.2f}",
            "bbox": [60, sum_y + 35, 200, sum_y + 60],
            "norm_bbox": [round(60/width, 4), round((sum_y+35)/height, 4), round(200/width, 4), round((sum_y+60)/height, 4)]
        },
        "total_deductions": {
            "label": "TOTAL DEDUCTIONS",
            "value": f"${total_deductions:,.2f}",
            "bbox": [280, sum_y + 35, 450, sum_y + 60],
            "norm_bbox": [round(280/width, 4), round((sum_y+35)/height, 4), round(450/width, 4), round((sum_y+60)/height, 4)]
        },
        "net_pay": {
            "label": "NET PAY",
            "value": net_pay_str,
            "bbox": [540, sum_y + 32, 750, sum_y + 65],
            "norm_bbox": [round(540/width, 4), round((sum_y+32)/height, 4), round(750/width, 4), round((sum_y+65)/height, 4)]
        }
    }

    metadata = {
        "document_type": "paystub",
        "width": width,
        "height": height,
        "employer": employer_name,
        "employee": employee_name,
        "gross_pay": gross_pay,
        "total_deductions": total_deductions,
        "net_pay": net_pay,
        "fields": field_metadata,
        "is_authentic": True,
        "attack_type": None
    }

    return image, metadata
