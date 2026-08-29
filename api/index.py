from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path


app = FastAPI(
    title="Football Player Value Prediction API",
    description="Predict football player market value using machine learning.",
    version="1.0"
)


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "model"
    / "football_player_value_deployment_pipeline.pkl"
)

PUBLIC_DIR = BASE_DIR / "public"


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# INPUT DATA
# --------------------------------------------------

class PlayerData(BaseModel):

    overall: int
    potential: int
    age: int
    international_reputation: int

    pace: float
    shooting: float
    passing: float
    dribbling: float

    physic: float
    skill_moves: int


# --------------------------------------------------
# PREDICTION API
# --------------------------------------------------

@app.post("/api/predict")
def predict(data: PlayerData):

    input_data = pd.DataFrame([{

        "overall": data.overall,
        "potential": data.potential,
        "age": data.age,
        "international_reputation": data.international_reputation,

        "pace": data.pace,
        "shooting": data.shooting,
        "passing": data.passing,
        "dribbling": data.dribbling,

        "physic": data.physic,
        "skill_moves": data.skill_moves

    }])

    prediction = model.predict(input_data)[0]

    return {
        "predicted_value_eur": float(prediction),
        "predicted_value_million": round(
            float(prediction) / 1_000_000,
            2
        )
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/api/health")
def health():

    return {
        "status": "OK",
        "message": "Football Player Value Prediction API is running"
    }


# --------------------------------------------------
# SERVE FRONTEND
# --------------------------------------------------

app.mount(
    "/",
    StaticFiles(
        directory=PUBLIC_DIR,
        html=True
    ),
    name="frontend"
)
