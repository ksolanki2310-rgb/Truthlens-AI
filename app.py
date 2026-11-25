
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.responses import FileResponse

# Create FastAPI application
app = FastAPI(title="Fake Job Detection")

# Load trained model
model = joblib.load("model.pkl")


# Input data structure
class Job(BaseModel):
    title: str
    company_profile: str = ""
    description: str = ""
    requirements: str = ""

    employment_type: str = "Unknown"
    required_experience: str = "Unknown"
    required_education: str = "Unknown"

    telecommuting: int = 0
    has_company_logo: int = 0
    has_questions: int = 0


# Home page
@app.get("/")
def home():
    return FileResponse("index.html")


# Prediction API
@app.post("/predict")
def predict(job: Job):

    # Combine text columns
    text = (
        f"{job.title} "
        f"{job.company_profile} "
        f"{job.description} "
        f"{job.requirements}"
    )

    # Create input dataframe
    row = pd.DataFrame([{
        "text": text,
        "employment_type": job.employment_type,
        "required_experience": job.required_experience,
        "required_education": job.required_education,
        "telecommuting": job.telecommuting,
        "has_company_logo": job.has_company_logo,
        "has_questions": job.has_questions
    }])

    # Predict probability
    prob = float(model.predict_proba(row)[0][1])

    # Fraud detection result

    fraudulent = int(prob >= 0.5)


    return {

        "fraudulent": fraudulent,

        "probability": round(prob, 2),

        "message": (

            "This job posting looks suspicious. Be careful!"

            if fraudulent == 1

            else "This job posting appears genuine."

            )
            }