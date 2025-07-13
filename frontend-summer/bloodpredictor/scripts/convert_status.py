import json

# Load thresholds from config file
with open("data/config/thresholds.json") as f:
    THRESHOLDS = json.load(f)

def convert_status(test_name, value):
    thresholds = THRESHOLDS[test_name]
    labels = list(thresholds.keys())
    limits = list(thresholds.values())

    for i in range(len(labels) - 1):
        if value < limits[i + 1]:
            return labels[i]
    return labels[-1]  # If value > highest limit
