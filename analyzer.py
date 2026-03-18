
from config import LAB_PARAMETERS

#Analyze single parameter
def analyze_parameter(name, value, gender):
  param = LAB_PARAMETERS[name]

  #Choose correct range
  if gender in param:
    min_val, max_val = param[gender]
  else:
    min_val, max_val = param["default"]

  #Determine status
  status = "Normal"
  if value < min_val:
    status = "Low"
  elif value > max_val:
    status = "High"

  return {
      "name": name,
      "value": value,
      "status": status,
      "normal_range": f"{min_val} - {max_val} {param['unit']}",
      "risk_weight": param["risk_weight"]
  }

#Analyze full report
def analyze_report(profile, lab_values):
  gender = profile["gender"]

  results = []
  total_risk = 0

  #BMI calculation
  height_m = profile["height"] / 100
  bmi = profile["weight"] / (height_m ** 2)

  for name, value in lab_values.items():
    if name in LAB_PARAMETERS:
      result = analyze_parameter(name, value, gender)
      results.append(result)

      if result["status"] != "Normal":
        total_risk += result["risk_weight"]
  
  #Risk level decision
  risk_level = "Low"
  if total_risk > 30:
    risk_level = "High"
  elif total_risk > 15:
    risk_level = "Moderate"

  return {
      "risk_score": total_risk,
      "risk_level": risk_level,
      "bmi": round(bmi, 2),
      "parameters": results
  }
