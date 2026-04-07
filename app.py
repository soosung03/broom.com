from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="Car Deal Advisor API")
app.mount("/static", StaticFiles(directory="static"), name="static")


class EvaluateRequest(BaseModel):
    brand: str = Field(min_length=1)
    model: str = Field(min_length=1)
    year: int = Field(ge=1990, le=2030)
    mileage: int = Field(ge=0)
    price: float = Field(gt=0)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(Path("static/index.html"))


@app.post("/api/evaluate")
def evaluate_deal(payload: EvaluateRequest) -> dict:
    current_year = datetime.utcnow().year
    age = max(0, current_year - payload.year)

    # A simple baseline expected value model (to be replaced with real market data)
    estimated_base = 35000
    age_penalty = age * 1400
    mileage_penalty = (payload.mileage / 10000) * 900
    expected_price = max(3000, estimated_base - age_penalty - mileage_penalty)

    ratio = payload.price / expected_price
    if ratio <= 0.9:
        score = 90
        verdict = "Great deal"
    elif ratio <= 1.1:
        score = 75
        verdict = "Fair deal"
    else:
        score = 55
        verdict = "Potentially overpriced"

    if payload.year >= current_year - 5:
        year_quality = "Strong recent model year"
    elif payload.year >= current_year - 10:
        year_quality = "Generally good model year"
    else:
        year_quality = "Older year: inspect service history carefully"

    confidence = 0.7 if age <= 10 else 0.6

    reasoning = (
        f"Estimated market baseline for this profile is around ${expected_price:,.0f}. "
        f"Your listed price is ${payload.price:,.0f}. "
        "Use this as a first-pass screen before inspection and VIN/history checks."
    )

    return {
        "score": score,
        "verdict": verdict,
        "year_quality": year_quality,
        "reasoning": reasoning,
        "confidence": confidence,
    }
