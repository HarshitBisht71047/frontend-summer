import json
import os

# Load interpretation rules
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RULES_FILE = os.path.join(BASE_DIR, "data", "config", "cbc_interpretation_rules.json")

with open(RULES_FILE, "r") as f:
    interpretation_rules = json.load(f)

def analyze_parameters(input_dict):
    """
    Analyze CBC parameters and return explanation for each.
    """
    explanations = []
    for key, value in input_dict.items():
        if "_status" in key:
            rule = interpretation_rules.get(key, {})
            message = rule.get(value, f"{key} = {value}")
            explanations.append(f"{key} = {value} → {message}")
    return explanations
