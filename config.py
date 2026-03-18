
# This file contains medical rules (normal ranges)

LAB_PARAMETERS = {
    "hemoglobin": {
        "male": (13.5, 17.5),
        "female": (12.0, 15.5),
        "unit": "g/dL",
        "risk_weight": 10
    },
    "fasting_glucose": {
        "default": (70, 99),
        "unit": "mg/dL",
        "risk_weight": 15
    },
    "cholesterol_total": {
        "default": (0, 200),
        "unit": "mg/dL",
        "risk_weight": 15
    },
    "vitamin_d": {
        "default": (30, 100),
        "unit": "ng/mL",
        "risk_weight": 8
    }
}
