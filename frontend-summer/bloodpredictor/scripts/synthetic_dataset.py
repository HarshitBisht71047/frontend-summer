import json
import random
import pandas as pd
from tqdm import tqdm

# ------------ CONFIG ------------
NUM_ROWS_PER_DISEASE = 60
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

FEATURE_FILE = "Version 4/data/config/feature_list.json"
RULE_FILE = "Version 4/data/config/disease_rules.json"
OUTPUT_FILE = "Version 4/data/processed/cbc_dataset_final.csv"
# --------------------------------

# ✅ Load Features & Status Choices
with open(FEATURE_FILE, "r") as f:
    features = json.load(f)

cbc_columns = features["cbc_columns"]
symptom_columns = features["symptom_columns"]
status_choices = features["status_choices"]

# ✅ Load Disease Rules
with open(RULE_FILE, "r") as f:
    disease_rules = json.load(f)

data_rows = []

for disease, rules in tqdm(disease_rules.items(), desc="Generating data"):
    for _ in range(NUM_ROWS_PER_DISEASE):
        row = {}

        # 🔹 CBC Features
        for col in cbc_columns:
            if col in rules:
                row[col] = random.choice(rules[col])
            else:
                row[col] = random.choice(status_choices[col])

        # 🔹 Symptoms
        for symptom in symptom_columns:
            if "symptoms" in rules:
                if rules["symptoms"] == ["any"]:
                    row[symptom] = random.choice([0, 1])
                else:
                    row[symptom] = int(symptom in rules["symptoms"])
            else:
                row[symptom] = random.choice([0, 1])

        # 🔹 Label
        row["Disease"] = disease
        data_rows.append(row)

# ✅ Save CSV
df = pd.DataFrame(data_rows)
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Dataset generated with {len(df)} rows → saved to '{OUTPUT_FILE}'")
