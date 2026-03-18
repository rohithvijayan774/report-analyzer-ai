
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
      text += page.extract_text() + "\n"

  #Extract values using regex
  lab_values = {}

  def extract_value(pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    return float(match.group(1)) if match else None

  #Simple extraction rules (can improve later)
  lab_values["hemoglobin"] = extract_value(r"hemoglobin\s*[:\-]?\s*(\d+\.?\d*)")
  lab_values["fasting_glucose"] = extract_value(r"glucose\s*[:\-]?\s*(\d+\.?\d*)")
  lab_values["cholesterol_total"] = extract_value(r"cholesterol\s*[:\-]?\s*(\d+\.?\d*)")
  lab_values["vitamin_d"] = extract_value(r"vitamin\s*d\s*[:\-]?\s*(\d+\.?\d*)")

  #Remove None values
  lab_values = {k: v for k, v in lab_values.items() if v is not None}

  #Dummy profile (later from user input)
  profile = {
      "gender": "male",
      "age": 30,
      "weight": 70,
      "height":170
  }

  result = analyze_report(profile, lab_values)

  return {
      "extracted_values": lab_values,
      "analysis": result
  }
