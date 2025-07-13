from models.predictor import predict_diseases
from utils.analyze_parameters import analyze_parameters  # ✅ Step 1

# ----------------------------------------
# Input Dictionary
# ----------------------------------------
input_dict = {
    "HGB_status": "Normal",
    "RBC_status": "Normal",
    "MCV_status": "Normal",
    "WBC_status": "Normal",
    "NEUT_status": "Normal",
    "LYM_status": "Low",
    "PLT_status": "Low",
    "Fatigue": 0,
    "Dizziness": 0,
    "Paleness": 0,
    "Shortness_of_breath": 0,
    "Tingling": 0,
    "Bleeding_tendency": 0,
    "Muscle_weakness": 0,
    "Fever": 1,
    "Chills": 1,
    "Nausea": 0,
    "Swelling": 0,
    "Chest_discomfort": 0
}

# ----------------------------------------
# Step 1: Rule-based CBC Interpretation
# ----------------------------------------
print("🔍 CBC Interpretation Based on Status:")
cbc_explanations = analyze_parameters(input_dict)
for line in cbc_explanations:
    print("📌", line)

print("\n🤖 Predicting Most Likely Conditions...\n")

# ----------------------------------------
# Step 2: Disease Prediction + Explanation
# ----------------------------------------
results = predict_diseases(input_dict)

# -------------------------------
# Step 2: Display Prediction Output Cleanly
# -------------------------------
print("\n🔎 Final Diagnosis Summary\n")

for idx, r in enumerate(results, 1):
    print(f"{idx}. {r['condition']} ({r['probability']})")

    # Advice Section
    if r.get("advice"):
        print(f"   🩺 Note: {r['advice']}")

    # Diet Recommendations
    if r.get("diet"):
        print(f"   🍽️ Suggested Diet: {r['diet']}")

    # Follow-Up Tests
    if r.get("follow_up_tests"):
        tests = ', '.join(r['follow_up_tests'])
        print(f"   🧪 Recommended Tests: {tests}")
    
    print()  # Blank line for separation
