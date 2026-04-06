
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Dict
import re
import pdfplumber

from analyzer import analyze_report

app = FastAPI()

#------------------------
#Request Model (JSON input)
#------------------------
class Profile(BaseModel):
  gender: str
  age: int
  weight: float
  height: float

class AnalyzeRequest(BaseModel):
  profile: Profile
  lab_values: Dict[str, float]

#------------------------
#Home Route
#------------------------
@app.get("/")
def home():
  return {"message": "Health AI running"}

#------------------------
#Manual JSON API
#------------------------
@app.post("/analyze")
def analyze(data: AnalyzeRequest):
  return analyze_report(
      data.profile.dict(),
      data.lab_values
  )

#------------------------
#PDF Upload API
#------------------------
@app.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):

  text = ""

  #Read PDF
  with pdfplumber.open(file.file) as pdf:
    for page in pdf.pages:
      text += (page.extract_text() or "") + "\n"

  print(text[:500])

  #Extract values using regex
  lab_values = {}

  def extract_value(pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    return float(match.group(len(match.groups()))) if match else None

  #Simple extraction rules (can improve later)
  lab_values["hemoglobin"] = extract_value(r"(hemoglobin|hb|hgb)\s*[:\-]?\s*(\d+\.?\d*)")
  lab_values["fasting_glucose"] = extract_value(r"(glucose|fasting glucose)\s*[:\-]?\s*(\d+\.?\d*)")
  lab_values["cholesterol_total"] = extract_value(r"(cholesterol|total cholesterol)\s*[:\-]?\s*(\d+\.?\d*)")
  lab_values["vitamin_d"] = extract_value(r"(vitamin\s*d|vit d)\s*[:\-]?\s*(\d+\.?\d*)")

  #Remove None values
  lab_values = {k: v for k, v in lab_values.items() if v is not None}

  if not lab_values:
      return {
          "status": "error",
          "message": "No lab values detected"
      }

  #Dummy profile (later from user input)
  profile = {
      "gender": "male",
      "age": 30,
      "weight": 70,
      "height":170
  }

  result = analyze_report(profile, lab_values)

  return {
      "status": "success",
      "extracted_values": lab_values,
      **result
  }
