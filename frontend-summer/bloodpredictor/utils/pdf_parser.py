import fitz  # PyMuPDF
import re

def extract_input_dict_from_pdf(filepath):
    text = ""
    
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()

    def extract_value(pattern, multiplier=1):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            val = float(match.group(1))
            return round(val * multiplier, 2)
        return None

    def classify(value, normal_range):
        if value is None:
            return "Unknown"
        if value < normal_range[0]:
            return "Low"
        elif value > normal_range[1]:
            return "High"
        else:
            return "Normal"

    # ✅ Extract values using better regex
    hgb = extract_value(r"Haemoglobin\s*[:\-]?\s*(\d+\.?\d*)")
    rbc = extract_value(r"Total RBC Count\s*[:\-]?\s*(\d+\.?\d*)")
    mcv = extract_value(r"MCV\s*[:\-]?\s*(\d+\.?\d*)")
    wbc = extract_value(r"Total Leucocyte Count\s*[:\-]?\s*(\d+\.?\d*)")
    neut = extract_value(r"Neutrophils\s*[:\-]?\s*(\d+\.?\d*)")
    lym = extract_value(r"Lymphocytes\s*[:\-]?\s*(\d+\.?\d*)")
    plt = extract_value(r"Platelet Count\s*[:\-]?\s*(\d+\.?\d*)", multiplier=100)  # lakhs → 100K

    input_dict = {
        "HGB": hgb,
        "HGB_status": classify(hgb, (12.0, 16.0)),
        "RBC": rbc,
        "RBC_status": classify(rbc, (3.9, 4.8)),
        "MCV": mcv,
        "MCV_status": classify(mcv, (83.0, 101.0)),
        "WBC": wbc,
        "WBC_status": classify(wbc, (4000, 11000)),
        "NEUT": neut,
        "NEUT_status": classify(neut, (45.0, 70.0)),
        "LYM": lym,
        "LYM_status": classify(lym, (20.0, 40.0)),
        "PLT": plt,
        "PLT_status": classify(plt, (150000, 450000)),
    }

    # Add symptoms from UI (placeholder)
    return input_dict
